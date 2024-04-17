"""Users table resources"""

import uuid
from sqlite3 import IntegrityError
from typing import Any, Dict, List, Tuple, Union

from flask_restful import Resource, reqparse

from financify_api.library.db_connector import (
    db_build_record,
    db_build_table,
    db_commit_change,
    db_fetchall,
    db_fetchone,
    db_get_schema,
)
from financify_api.library.security import admin_required


class Users(Resource):  # type: ignore [misc]
    """users table resource for admins only"""

    def __init__(self) -> None:
        super().__init__()
        self.table = "users"
        self.schema = db_get_schema(self.table)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username")

    @admin_required
    def get(self, user_id: int = 0) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """get user table"""
        if user_id != 0:
            user = db_fetchone(f"SELECT * FROM {self.table} WHERE id = ?", (user_id,))
            return db_build_record(fetch=user, schema=self.schema)
        response = db_fetchall(f"SELECT * FROM {self.table}")
        return db_build_table(fetch=response, schema=self.schema)

    @admin_required
    def post(self) -> Tuple[Dict[str, Any], int]:
        """create a new user and return the user API key"""
        args = self.parser.parse_args()
        if not args["username"]:
            return ({"error": "no username provided"}, 400)
        try:
            api_key = uuid.uuid4().hex
            db_commit_change(
                f"INSERT INTO {self.table} (username, password) VALUES (?, ?)",
                (args["username"], api_key),
            )
            user = db_fetchone(
                f"SELECT * FROM {self.table} WHERE username = ?", (args["username"],)
            )
            return (db_build_record(fetch=user, schema=self.schema), 201)
        except IntegrityError:
            return ({"error": "username already taken"}, 409)
