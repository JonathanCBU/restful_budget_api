"""database setup for tests"""

import os
import sqlite3


def make_db(schema_file: str, db_name: str) -> str:
    """create test db file and return path name

    :param schema_file: file name withough .sql extension
    :param db_name: name of db file to create without .db extenstion
    """
    db_file = os.path.join(os.path.dirname(__file__), f"../{db_name}.db")
    db_client = sqlite3.connect(db_file)
    schema_file = os.path.join(os.path.dirname(__file__), f"../schemas/{schema_file}.sql")
    with open(schema_file, "r", encoding="utf-8") as schema:
        db_client.executescript(schema.read())
    db_client.close()
    return db_file
