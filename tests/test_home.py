"""test the home endpoint"""

import requests
import pytest


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_home(base_access_app):
    """test home endpoint"""
    resp = requests.get("http://127.0.0.1:5000/home")
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
