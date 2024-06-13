"""config functions for unit tests"""

import os
from multiprocessing import Process
from typing import Dict, Iterator, List, Union

import pytest

from financify_api.__app__ import create_api, create_app
from tests.library.db_setup import make_db
import time

@pytest.fixture
def admin_access_app(request: pytest.FixtureRequest) -> Iterator[Union[Process, str]]:
    """launch admin server with user creation perms"""
    test_db = make_db(request.param, "admin_tester")
    args = {"admin": True, "database": test_db}
    app = create_app(args)
    _ = create_api(app)
    app_process = Process(target=app.run, kwargs={"debug": False})
    app_process.start()
    yield app_process
    app_process.terminate()
    os.remove(test_db)
    time.sleep(3)

@pytest.fixture
def base_access_app(request: pytest.FixtureRequest) -> Iterator[Union[Process, str]]:
    """launch admin server with user creation perms"""
    test_db = make_db(request.param, "base_tester")
    args = {"admin": False, "database": test_db}
    app = create_app(args)
    _ = create_api(app)
    app_process = Process(target=app.run, kwargs={"debug": False})
    app_process.start()
    yield app_process
    app_process.terminate()
    os.remove(test_db)
    time.sleep(3)

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
def dummy_patterns() -> Dict[str, str]:
    """return list of dummy patterns"""
    return {"title": "Pattern 1", "date": r"\d{4}-\d{2}", "value": r"\$(\d{3,9}\.\d{2}"}
