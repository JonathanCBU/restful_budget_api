"""patterns table resources"""

from typing import Any, Dict, List, Tuple, Union

from flask_restful import Resource, reqparse, request

from restful_budget_api.library.db_connector import (
    db_add_new_record,
    db_build_record,
    db_build_table,
    db_fetchall,
    db_fetchone,
    db_get_schema,
)


class Patterns(Resource):  # type: ignore [misc]
    """patterns table resource"""

    def __init__(self) -> None:
        super().__init__()
        self.table = "patterns"
        self.schema = db_get_schema(self.table)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("title", type=str)
        self.parser.add_argument("date", type=str)
        self.parser.add_argument("value", type=str)

    def get(self) -> Tuple[Union[Dict[str, Any], List[Dict[str, Any]]], int]:
        """get whole table or record by id or title

        :param title_or_id: title field value
        """
        patterns = db_fetchall(f"SELECT * FROM {self.table}")
        return (db_build_table(fetch=patterns, schema=self.schema), 200)

    def post(self) -> Tuple[Dict[str, Any], int]:
        """add new pattern to table"""
        print(request.json)
        args = self.parser.parse_args()
        args["title"] = args["title"].lower()
        for field, val in args.items():
            if not val:
                return ({"error": f"field {field} not provided"}, 400)
        record = db_add_new_record(table=self.table, insert=args)
        return (record, 201)


class PatternsById(Resource):  # type: ignore [misc]
    """get patterns by ID"""

    def __init__(self) -> None:
        super().__init__()
        self.table = "patterns"
        self.schema = db_get_schema(self.table)

    def get(self, id_num: int) -> Tuple[Dict[str, Any], int]:
        """get pattern record

        :param id_num: pattern id
        """
        pattern = db_fetchone(
            f"SELECT * FROM {self.table} WHERE id = ?", (id_num,)
        )
        return (db_build_record(fetch=pattern, schema=self.schema), 200)


class PatternsByTitle(Resource):  # type: ignore [misc]
    """get patterns by title"""

    def __init__(self) -> None:
        super().__init__()
        self.table = "patterns"
        self.schema = db_get_schema(self.table)

    def get(self, title: str) -> Tuple[Dict[str, Any], int]:
        """get pattern record

        :param title: pattern title (not case sensitive)
        """
        pattern = db_fetchone(
            f"SELECT * FROM {self.table} WHERE title = ?", (title.lower(),)
        )
        return (db_build_record(fetch=pattern, schema=self.schema), 200)
