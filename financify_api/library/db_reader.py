"""Class for reading from financify DBs"""

import os
import sqlite3
from typing import List, Tuple, Any, Union
from dataclasses import dataclass


@dataclass
class StatementRecord:
    """Statement record data type"""

    date: str
    value: float
    asset_type: str


class FinancifyDb:
    """Python wrappings around SQLite queries"""

    def __init__(self, db_path: str, make_new: bool = False) -> None:
        """Connect to db

        :param db_path: abspath to database file
        :param make_new: create new database if true
        """
        if make_new:
            # make new database but fail if the parent dir already exists
            os.makedirs(os.path.dirname(db_path), exist_ok=False)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def _query(
        self, sql: List[str], parameters: Union[List[Tuple[Any]], None] = None
    ) -> sqlite3.Cursor:
        """Execute query

        :param sql: list of SQLite statements
        """
        if parameters is not None:
            response = self.cursor.executemany(" ".join(sql), parameters)
        else:
            response = self.cursor.execute(" ".join(sql))
        return response

    def get_table(self, table: str, order: str = "") -> List[StatementRecord]:
        """Get all rows of a table

        :param table: table name
        :param order: column to order response by
        """
        if order:
            response = self._query(
                ["SELECT * FROM", table, f"ORDER BY {order}"]
            ).fetchall()
        else:
            response = self._query(["SELECT * FROM", table]).fetchall()
        return [
            StatementRecord(date=row[0], asset_type=row[1], value=row[2])
            for row in response
        ]
