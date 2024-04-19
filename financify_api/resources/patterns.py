"""patterns table resources"""

from typing import Any, Dict, List, Tuple, Union

from flask_restful import Resource, reqparse, request

from financify_api.library.db_connector import (
    db_build_record,
    db_build_table,
    db_commit_change,
    db_fetchall,
    db_fetchone,
    db_get_schema,
    db_next_id,
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

    def get(
        self, title_or_id: str = ""
    ) -> Tuple[Union[Dict[str, Any], List[Dict[str, Any]]], int]:
        """get whole table or record by id or title

        :param title_or_id: title field value
        """
        if not title_or_id:
            patterns = db_fetchall(f"SELECT * FROM {self.table}")
            return (db_build_table(fetch=patterns, schema=self.schema), 200)
        try:
            title_or_id = int(title_or_id)
            where_field = "id"
        except ValueError:
            where_field = "title"
        pattern = db_fetchone(
            f"SELECT * FROM {self.table} WHERE {where_field} = ?", (title_or_id,)
        )
        return (db_build_record(fetch=pattern, schema=self.schema), 200)

    def post(self) -> Tuple[Dict[str, Any], int]:
        """add new pattern to table"""
        print(request.json)
        args = self.parser.parse_args()
        for field, val in args.items():
            if not val:
                return ({"error": f"field {field} not provided"}, 400)
        record_id = db_next_id(self.table)
        db_commit_change(
            sql=f"INSERT INTO {self.table} "
            f"({', '.join(args.keys())}) "
            f"VALUES ({', '.join(['?' for _ in args])})",
            data=tuple(args.values()),
        )
        fetch = db_fetchone(
            sql=f"SELECT * FROM {self.table} WHERE id = ?",
            data=(record_id,),
        )
        record = db_build_record(fetch=fetch, schema=self.schema)
        return (record, 201)


"""
 "val": r"Your Portfolio Value: \$(\d{1,9}\.\d{2})",
        "date": r"[A-Za-z]{3,9} \d{1,2} \d{4} - ([A-Za-z]{3,9} \d{1,2} \d{4})",
"""
