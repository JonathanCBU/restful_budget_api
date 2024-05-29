"""statements tables resources"""

from typing import Any, Dict, List, Tuple

from flask_restful import Resource, reqparse

from financify_api.library.db_connector import (
    db_add_new_record,
    db_build_record,
    db_build_table,
    db_commit_change,
    db_fetchall,
    db_fetchone,
    db_get_schema,
    db_ids,
)
from financify_api.library.security import api_key_required, get_user, strict_verbiage


class Statements(Resource):  # type: ignore [misc]
    """assets and liabilities table resource"""

    def __init__(self, table: str, parser: reqparse.RequestParser) -> None:
        super().__init__()
        self.parser = parser
        self.table = table
        self.schema = db_get_schema(self.table)

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
        args = self.parser.parse_args()
        for field, val in args.items():
            if not val:
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
        valid_ids = db_ids(self.table)
        if record_id not in valid_ids:
            return ({"error": f"{self.table} id invalid"}, 400)
        user_id = get_user()
        record = db_build_record(
            fetch=db_fetchone(
                sql=f"SELECT * FROM {self.table} WHERE id = ?", data=(record_id,)
            ),
            schema=self.schema,
        )
        if user_id != record["user_id"]:
            return ({"error": f"no access to {self.table} id {record_id}"}, 403)
        db_commit_change(
            sql=f"DELETE FROM {self.table} WHERE id = ?", data=(record_id,)
        )
        return ({"table": self.table, "deleted_id": record_id}, 200)

    # TODO: Add an update method for changing statement report id number


class Liabilities(Statements):
    """Liabilities instance of statements"""

    def __init__(self) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("value", type=float)
        super().__init__(table="liabilities", parser=parser)


class Assets(Statements):
    """Assets instance of statements"""

    def __init__(self) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("description", type=str)
        parser.add_argument("value", type=float)
        super().__init__(table="assets", parser=parser)


class Reports(Statements):
    """Reports table resource"""

    def __init__(self) -> None:
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("net_worth", type=str)
        super().__init__(table="reports", parser=parser)
