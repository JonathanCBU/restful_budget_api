"""statements tables resources"""

from typing import Any, Dict, List, Tuple

from flask_restful import Resource, reqparse

from restful_budget_api.library.db_connector import (
    db_add_new_record,
    db_build_record,
    db_build_table,
    db_commit_change,
    db_fetchall,
    db_fetchone,
    db_get_schema,
    db_ids,
)
from restful_budget_api.library.security import api_key_required, get_user, strict_verbiage


class KeyRestricted(Resource):  # type: ignore [misc]
    """assets and liabilities table resource"""

    def __init__(self, table: str, parser: reqparse.RequestParser) -> None:
        super().__init__()
        self.parser = parser
        self.table = table
        self.schema = db_get_schema(self.table)

    def verify_record_id(self, record_id: int) -> bool:
        """verify entered record id is valid

        :param record_id: id number of record
        """
        valid_ids = db_ids(self.table)
        if record_id not in valid_ids:
            return False
        return True

    def verify_user_ownership(self, record_id: int) -> bool:
        """verify user created or otherwise owns record being edited

        :param record_id: id number of record
        """
        record = db_build_record(
            fetch=db_fetchone(
                sql=f"SELECT * FROM {self.table} WHERE id = ?", data=(record_id,)
            ),
            schema=self.schema,
        )
        if get_user() != record["user_id"]:
            return False
        return True

    @strict_verbiage
    @api_key_required
    def get(self) -> Tuple[List[Dict[str, Any]], int]:
        """return all table records"""
        user_id = get_user()
        response = db_fetchall(
            sql=f"SELECT * FROM {self.table} WHERE user_id = ?",
            data=(user_id,),
        )
        table = db_build_table(fetch=response, schema=self.schema)
        return (table, 200)

    @strict_verbiage
    @api_key_required
    def post(self) -> Tuple[Dict[str, Any], int]:
        """add new record to table"""
        required_args = ["date", "value", "description"]
        args = self.parser.parse_args()
        for field in required_args:
            if not args.get(field):
                return ({"error": f"field {field} not provided"}, 400)
        user_id = get_user()
        args["user_id"] = user_id
        record = db_add_new_record(table=self.table, insert=args)
        return (record, 201)

    @strict_verbiage
    @api_key_required
    def delete(self, record_id: int = 0) -> Tuple[Dict[str, Any], int]:
        """delete record by ID if api key allows for it

        :param record_id: id number of record to delete
        """
        if not self.verify_record_id(record_id):
            return ({"error": f"{self.table} id invalid"}, 400)
        if not self.verify_user_ownership(record_id):
            return ({"error": f"no access to {self.table} id {record_id}"}, 403)
        db_commit_change(
            sql=f"DELETE FROM {self.table} WHERE id = ?", data=(record_id,)
        )
        return ({"table": self.table, "deleted_id": record_id}, 200)

    @strict_verbiage
    @api_key_required
    def patch(self, record_id: int = 0) -> Tuple[Dict[str, Any], int]:
        """Update report ID key for assets and liabilities

        :param record_id: id number of record to change
        """
        if self.table == "reports":
            return ({"error": f"{self.table} does not have a patch method"}, 405)
        if not self.verify_record_id(record_id):
            return ({"error": f"{self.table} id invalid"}, 400)
        if not self.verify_user_ownership(record_id):
            return ({"error": f"no access to {self.table} id {record_id}"}, 403)
        args = self.parser.parse_args()
        if not args.get("report_id"):
            return ({"error": "field report_id not provided"}, 400)
        db_commit_change(
            sql=f"UPDATE {self.table} SET report_id = ? WHERE id = ?",
            data=(args["report_id"], record_id),
        )
        return ({"table": self.table, "updated_id": record_id}, 200)


class Statements(KeyRestricted):
    """Financial Statements parent resource"""

    def __init__(self, table: str) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("value", type=float)
        parser.add_argument("report_id", type=int)
        super().__init__(table=table, parser=parser)


class Liabilities(Statements):
    """Liabilities instance of statements"""

    def __init__(self) -> None:
        super().__init__(table="liabilities")


class Assets(Statements):
    """Assets instance of statements"""

    def __init__(self) -> None:
        super().__init__(table="assets")


class Reports(KeyRestricted):
    """Reports table resource"""

    def __init__(self) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("net_worth", type=str)
        super().__init__(table="reports", parser=parser)
