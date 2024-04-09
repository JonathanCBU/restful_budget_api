"""Pull data from assets and liabilities and update reports as needed"""

from financify_api.library.db_reader import FinancifyDb
import dotenv
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Any, Dict

dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
)


@dataclass
class Statement:
    """Assets and Liabilities schema"""

    id_num: int
    date: datetime
    description: str
    value: float
    used: bool


@dataclass
class Report:
    """Reports schema"""

    id_num: int
    date: str
    asset_ids: str
    liability_ids: str
    net_worth: float


def main() -> None:
    """Main pipeline function"""
    db_client = FinancifyDb(os.environ["FINANCIFY_DB"])
    assets = db_client.get_table("assets")
    liabilities = db_client.get_table("liabilities")
    reports = db_client.get_table("reports")

    reports_map, reports_records = parse_reports(reports)
    asset_records = parse_statements(assets)
    unused_asset_records = [record for record in asset_records if not record.used]
    liability_records = parse_statements(liabilities)
    unused_liability_records = [
        record for record in liability_records if not record.used
    ]
    if len(unused_asset_records) == 0 and len(unused_liability_records) == 0:
        print("No un-reported statements to process!")
        return

    unused_asset_records.sort(key=lambda record: record.date, reverse=False)
    unused_liability_records.sort(key=lambda record: record.date, reverse=False)

    asset_buckets = bucket_by_date(unused_asset_records)
    liability_buckets = bucket_by_date(unused_liability_records)

    new_reports = []
    next_id = reports_records[-1][0] + 1 if len(reports_records) > 0 else 1
    for date_key, records in asset_buckets.items():
        if date_key in liability_buckets:
            liabs = liability_buckets[date_key]
        # check if date key exists in records
        if date_key not in reports_map.values():
            # new report to make
            new_reports.append(assemble_report(next_id, date_key, records, liabs))
            next_id += 1

    # push new reports to table
    reps = [
        (rep.id_num, rep.date, rep.asset_ids, rep.liability_ids, rep.net_worth)
        for rep in new_reports
    ]
    db_client.insert(
        "reports", ["id", "date", "asset_ids", "liability_ids", "net_worth"], reps
    )

    # update statement records used for report gen
    db_client.update_by_id(
        "assets", "used", True, [str(asset.id_num) for asset in unused_asset_records]
    )
    db_client.update_by_id(
        "liabilities",
        "used",
        True,
        [str(liability.id_num) for liability in unused_liability_records],
    )
    db_client.commit()


def assemble_report(
    id_num: int, date_key: str, assets: List[Statement], liabilities: List[Statement]
) -> Report:
    """Create report instance

    :param id_num: unique id number to assign to report
    :param date_key: YYYY-MM date string
    :param assets: list of assets from the same month
    :param liabilities: list of liabilities from the same month
    """
    net_worth = 0
    asset_ids = ""
    liability_ids = ""
    for asset in assets:
        net_worth += asset.value
        asset_ids += f"{asset.id_num};"
    for liability in liabilities:
        net_worth -= liability.value
        liability_ids += f"{liability.id_num};"
    return Report(
        id_num=id_num,
        date=date_key,
        asset_ids=asset_ids,
        liability_ids=liability_ids,
        net_worth=round(
            net_worth, 2
        ),  # this is where I might get a rounding error but oh well idc
    )


def parse_statements(statements: List[Tuple[Any]]) -> List[Statement]:
    """Parse DB statement records

    :param statements: DB table response from assets or liabilities
    """
    # can't guarantee the order of query returns so we sort by type
    statement_list = []
    for statement in statements:
        # Because we know the table schema I am comfortable being strict here
        statement_list.append(
            Statement(
                id_num=statement[0],
                date=datetime.strptime(statement[1], "%Y-%m-%d"),
                description=statement[2],
                value=statement[3],
                used=bool(statement[4]),
            )
        )
    return statement_list


def parse_reports(
    reports_table: List[Tuple[Any]],
) -> Tuple[Dict[int, str], List[Report]]:
    """Parse existing reports to check for duplicates

    :param reports_table: response from reports table query
    """
    reports_list = []
    dates_map = {}
    for report in reports_table:
        reports_list.append(
            Report(
                id_num=report[0],
                date=report[1],
                asset_ids=report[2],
                liability_ids=report[3],
                net_worth=report[4],
            )
        )
        dates_map[report[0]] = report[1]
    return (dates_map, reports_list)


def bucket_by_date(statements: List[Statement]) -> Dict[int, List[Statement]]:
    """Return a dictionary of bucketed statements by month and year

    :param statements: list of statement records
    """
    buckets = {}
    for record in statements:
        report_key = f"{record.date.year}-{record.date.month:02}"
        if report_key not in buckets:
            buckets[report_key] = [record]
        else:
            buckets[report_key].append(record)
    return buckets
