"""Pull data from assets and liabilities and update reports as needed"""

from financify_api.library.db_reader import FinancifyDb
import dotenv
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Any

dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")
)


@dataclass
class Statement:
    """Assets and Liabilities schema"""

    id_num: int = 0
    date: str = ""
    description: str = ""
    value: float = 0.00


@dataclass
class Report:
    """Reports schema"""

    id_num: int = 0
    date: str = ""
    asset_ids: str = ""
    liability_ids: str = ""
    net_worth: float = 0.00


def main() -> None:
    """Main pipeline function"""
    print(os.environ["FINANCIFY_DB"])
    db_client = FinancifyDb(os.environ["FINANCIFY_DB"])
    assets = db_client.get_table("assets")
    liabilities = db_client.get_table("liabilities")

    asset_records = parse_statements(assets)
    liability_records = parse_statements(liabilities)

    print(asset_records)
    print(liability_records)


def parse_statements(statements: List[Tuple[Any]]) -> List[Statement]:
    """Parse DB statement records

    :param statements: DB table response from assets or liabilities
    """
    # can't guarantee the order of query returns so we sort by type
    statement_list = []
    for statement in statements:
        rec = Statement()
        for field in statement:
            if isinstance(field, int):
                rec.id_num = field
            elif type(field) == str and "-" in field:
                rec.date = field
            elif type(field) == str and "-" not in field:
                rec.description = field
            elif type(field) == float:
                rec.value = field
            else:
                raise TypeError(
                    f"Data field {field} in record {statement} not parsed to expected type"
                )
        statement_list.append(rec)
    return statement_list
