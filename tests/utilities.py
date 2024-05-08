"""config functions for unit tests"""

import pytest
import os
import sqlite3
from financify_api.__app__ import create_api, create_app


def test_db() -> str:
    """create test db file and return path name"""
    db_file = os.path.join(os.path.dirname(__file__), "temp_db.db")
    if os.path.exists(db_file):
        print("DB file already exists, removing...")
        os.remove(db_file)
    db_client = sqlite3.connect(db_file)
    schema_file = os.path.join(os.path.dirname(__file__), "../financify_api/schema.sql")
    with open(schema_file, "r", encoding="utf-8") as schema:
        db_client.executescript(schema.read())
    db_client.close()
    return db_file


def app():

    app = create_app()
    api = create_api()
    print(api.resources)
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
