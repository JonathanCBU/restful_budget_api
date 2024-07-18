"""test the home endpoint"""

# pylint: disable=unused-argument
from multiprocessing import Process

import requests

from tests.library import test_globals


def test_home(base_access_app: Process) -> None:
    """test home endpoint"""
    resp = requests.get(f"{test_globals.DEFAULT_URL}/home", timeout=5)
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
