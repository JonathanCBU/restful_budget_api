from tests.tst_utils import admin_server, tmp_db, dummy_users
import requests
import json

def test_new_users(tmp_db, admin_server, dummy_users) -> None:
   # """Initialize new users"""
    empty_resp = requests.get("http://127.0.0.1:5000/users") 
   # print(empty_resp.reason)
   # assert empty_resp.status_code == 200
    assert empty_resp.json() == []

   # users_resps = []
   # for user in dummy_users:
   #     resp = requests.post("http://127.0.0.1:5000/users", data=json.dumps({"username": user}), headers={"Content-Type": "application/json"})
   #     assert resp.status_code == 201
   #     print(resp.json())
