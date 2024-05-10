"""users endpoint testing"""

# pylint: disable=unused-argument
import json
from multiprocessing import Process
from typing import List

import pytest
import requests


@pytest.mark.parametrize("admin_access_app", ["users_schema"], indirect=True)
def test_user_access(admin_access_app: Process, dummy_users: List[str]) -> None:
    """App allows read/write access to user info when in admin mode"""
    empty_resp = requests.get(pytest.global_url, timeout=5)
    assert empty_resp.status_code == 200
    assert empty_resp.json()[0] == {"id": 1, "username": "tester_1", "password": "pwd1"}
    for user in dummy_users:
        resp = requests.post(
            pytest.global_url,
            data=json.dumps({"username": user}),
            headers=pytest.global_headers,
            timeout=5,
        )
        assert resp.status_code == 201


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_user_restriction(base_access_app: Process) -> None:
    """App does not return user information when server is not in admin mode"""
    resp = requests.get(pytest.global_url, timeout=5)
    breakpoint()
    assert resp.status_code == 403
    assets = requests.get(
        pytest.global_url,
        data=json.dumps({"api_key": "pwd1"}),
        headers=pytest.global_headers,
        timeout=5,
    )
    assert assets.status_code == 200
