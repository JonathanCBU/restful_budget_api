"""config functions for unit tests"""

import os
import time
from multiprocessing import Process
from typing import Dict, Iterator, List, Union

import pytest

from financify_api.__app__ import create_api, create_app
from tests.library.db_setup import make_db


@pytest.fixture
def admin_access_app(request: pytest.FixtureRequest) -> Iterator[Union[Process, str]]:
    """launch admin server with user creation perms"""
    test_db = make_db(request.param, "admin_tester")
    args = {"admin": True, "database": test_db}
    app = create_app(args)
    _ = create_api(app)
    app_process = Process(target=app.run, kwargs={"debug": False})
    app_process.start()
    time.sleep(0.5)
    yield app_process
    app_process.terminate()
    os.remove(test_db)
    time.sleep(0.5)


@pytest.fixture
def base_access_app(request: pytest.FixtureRequest) -> Iterator[Union[Process, str]]:
    """launch admin server with user creation perms"""
    test_db = make_db(request.param, "base_tester")
    args = {"admin": False, "database": test_db}
    app = create_app(args)
    _ = create_api(app)
    app_process = Process(target=app.run, kwargs={"debug": False})
    app_process.start()
    time.sleep(0.5)
    yield app_process
    app_process.terminate()
    os.remove(test_db)
    time.sleep(0.5)


@pytest.fixture
def dummy_users() -> List[str]:
    """return dummy user names"""
    return ["John", "Jane", "God"]


@pytest.fixture
def dummy_expenses() -> List[Dict[str, Union[str, float]]]:
    """return a list of dummy assets"""
    return [
        {"date": "2021-01-07", "description": "dinner", "amount": 123.45},
        {"date": "2021-03-38", "description": "groceries", "amount": 68.56},
        {"date": "2022-12-12", "description": "rent", "amount": 1005.07},
    ]


