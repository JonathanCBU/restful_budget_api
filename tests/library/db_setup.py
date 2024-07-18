"""database setup for tests"""

import os
import sqlite3


def make_db(db_file: str) -> str:
    """create test db file and return path name

    :param db_file: absolute path to db file
    """
    db_client = sqlite3.connect(db_file)
    schema_file = os.path.join(
        os.path.dirname(__file__), f"../../restful_budget_api/schema.sql"
    )
    with open(schema_file, "r", encoding="utf-8") as schema:
        db_client.executescript(schema.read())
    db_client.close()
    return db_file


def insert_test_users(db_file: str) -> None:
    """force test users with defined creds into the users table

    :param db_file: absolute path the database file
    """
    db_client = sqlite3.connect(db_file)
    users = [
        (
            "tester_1",
            "pwd1",
        ),
        (
            "tester_2",
            "pwd2",
        ),
        (
            "tester_3",
            "pwd3",
        ),
    ]
    db_client.executemany("INSERT INTO users (username, password) VALUES (?,?)", users)
    db_client.commit() 
    db_client.close()
