"""test the home endpoint"""

# pylint: disable=unused-argument
from multiprocessing import Process

import pytest
import requests


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_home(base_access_app: Process) -> None:
    """test home endpoint"""
    resp = requests.get("http://127.0.0.1:5000/home", timeout=5)
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
