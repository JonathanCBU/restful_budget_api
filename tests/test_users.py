import json

import requests
import pytest

@pytest.mark.parametrize("admin_access_app", ["users_schema"], indirect=True)
def test_user_access(admin_access_app, dummy_users) -> None:
    """App allows read/write access to user info when in admin mode"""
    empty_resp = requests.get("http://127.0.0.1:5000/users")
    assert empty_resp.status_code == 200
    assert empty_resp.json()[0] == {"id": 1, "username": "tester_1", "password": "pwd1"}
    for user in dummy_users:
        resp = requests.post(
            "http://127.0.0.1:5000/users",
            data=json.dumps({"username": user}),
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 201


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_user_restriction(base_access_app) -> None:
    """App does not return user information when server is not in admin mode"""
    resp = requests.get("http://127.0.0.1:5000/users")
    assert resp.status_code == 403
    assets = requests.get(
        "http://127.0.0.1:5000/assets",
        data=json.dumps({"api_key": "pwd1"}),
        headers={"Content-Type": "application/json"},
    )
    assert assets.status_code == 200

