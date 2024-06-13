"""users endpoint testing"""

# pylint: disable=unused-argument
import json
from multiprocessing import Process
from typing import List

import pytest
import requests

from tests.library import test_globals


@pytest.mark.parametrize("admin_access_app", ["users_schema"], indirect=True)
def test_user_success(admin_access_app: Process, dummy_users: List[str]) -> None:
    """App allows read/write access to user info when in admin mode"""
    # verify get of defaut users in test db
    default_resp = requests.get(f"{test_globals.DEFAULT_URL}/users", timeout=5)
    assert default_resp.status_code == 200
    assert default_resp.json()[0] == {"id": 1, "username": "tester_1", "password": "pwd1"}
    
    # verify post of new users
    for user in dummy_users:
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/users",
            data=json.dumps({"username": user}),
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        assert resp.status_code == 201

    # verify delete of user
    all_users = requests.get(f"{test_globals.DEFAULT_URL}/users", timeout=5)
    del_one = requests.delete(f"{test_globals.DEFAULT_URL}/users/1", timeout=5)  
    assert del_one.status_code == 200
    current_users = requests.get(f"{test_globals.DEFAULT_URL}/users", timeout=5) 
    assert len(current_users.json()) == len(all_users.json())-1


@pytest.mark.parametrize("admin_access_app", ["users_schema"], indirect=True)
def test_user_errors(admin_access_app: Process, dummy_users: List[str]) -> None:
    """Test failure states of users resource"""
    # verify post failures
    user_info = {"not_a_username": "Qwerty"}
    resp = requests.post(f"{test_globals.DEFAULT_URL}/users", timeout=5, data=json.dumps(user_info), headers={"Content-Type": "application/json"})
    assert resp.status_code == 400
    assert resp.json()["error"] == "no username provided"
     
    user_info = {"username": "tester_1"}
    resp = requests.post(f"{test_globals.DEFAULT_URL}/users", timeout=5, data=json.dumps(user_info), headers={"Content-Type": "application/json"})
    assert resp.status_code == 409
    assert resp.json()["error"] == "username already taken"

    # verify delete failures
    resp = requests.delete(f"{test_globals.DEFAULT_URL}/users/1000", timeout=5)
    assert resp.status_code == 400
    assert resp.json()["error"] == "users id invalid"



@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_user_restriction(base_access_app: Process) -> None:
    """App does not return user information when server is not in admin mode"""
    resp = requests.get(f"{test_globals.DEFAULT_URL}/users", timeout=5)
    assert resp.status_code == 403
    assets = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert assets.status_code == 200
