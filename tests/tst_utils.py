"""config functions for unit tests"""

import os
import sqlite3
from multiprocessing import Process
from typing import Dict, Iterator, List, Union

import pytest

from financify_api.__app__ import create_api, create_app

"""
TODO: Use Yield fixtures

Notes:
    1. Yield fixtures can only have one yield
    2. Yield should return an object needed for testing
    3. At the end of testing Pytest goes backwards through yield fixtures and runs the code that comes after their yields
"""


@pytest.fixture
def admin_server() -> Iterator[Union[Process, str]]:
    """launch admin server with user creation perms"""
    args = {
        "admin": True,
        "database": os.path.join(
            os.path.dirname(__file__), "../financify_api/schema.sql"
        ),
    }
    app = create_app(args)
    api = create_api(app)
    app_process = Process(target=app.run, kwargs={"debug": False})
    app_process.start()
    yield app_process
    app_process.terminate()


@pytest.fixture
def tmp_db() -> Iterator[Union[sqlite3.Connection, str]]:
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
    yield db_file
    os.remove(db_file)


@pytest.fixture
def dummy_users() -> List[str]:
    """return dummy user names"""
    return ["John", "Jane", "God"]


@pytest.fixture
def dummy_assets() -> List[Dict[str, Union[str, float]]]:
    """return a list of dummy assets"""
    return [
        {"date": "2021-01", "description": "bank", "value": 1000.00},
        {"date": "2021-01", "description": "investments", "value": 1234.56},
        {"date": "2021-02", "description": "bank", "value": 1005.07},
    ]


@pytest.fixture
def dummy_liabilities() -> List[Dict[str, Union[str, float]]]:
    """return a list of dummy liabilities"""
    return [
        {"date": "2021-01", "description": "student debt", "value": 1000.00},
        {"date": "2021-02", "description": "mortgage", "value": 1205.09},
    ]


@pytest.fixture
def dummy_patterns() -> Dict[str, str]:
    """return list of dummy patterns"""
    return {"title": "Pattern 1", "date": r"\d{4}-\d{2}", "value": r"\$(\d{3,9}\.\d{2}"}
