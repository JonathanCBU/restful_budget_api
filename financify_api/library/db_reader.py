"""Class for reading from financify DBs"""

import os
import sqlite3
from typing import List, Tuple, Any, Union


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

    def commit(self) -> None:
        """Commit changes to DB"""
        self.connection.commit()

    def get_table(self, table: str, order: str = "") -> List[Tuple[Any]]:
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
        return response

    def make_table(
        self, table: str, configs: List[str], overwrite: bool = False
    ) -> None:
        """Create a table in the DB

        :param table: table name
        :param configs: column information and other table configurations
        :param overwrite:
            use the 'IF NOT EXISTS' statement to keep from erroring if table already exists
        """
        cmd = "CREATE TABLE IF NOT EXISTS" if overwrite else "CREATE TABLE"
        _ = self._query(sql=[cmd] + [table] + configs)

    def drop_table(self, table: str) -> None:
        """Drop a table from the db

        :param table: table name
        """
        self._query(["DROP TABLE", "IF EXISTS", table])

    def insert(self, table: str, columns: List[str], values: List[Tuple[Any]]):
        """Insert data into a db table

        :param table: table name
        :param columns: list of table keys in the same order as each value tuple
        :param values: list of tuples for each record (row) in key (column) order
        """
        col_str = f"({', '.join(columns)})"
        val_str = ""
        for _ in range(1, len(columns)):
            val_str += "?, "
        val_str = f"({val_str}?)"
        _ = self._query(
            sql=["INSERT INTO", table, col_str, f"VALUES{val_str}"], parameters=values
        )
