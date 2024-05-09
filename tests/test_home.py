"""test the home endpoint"""

from tst_utils import admin_server
import requests

def test_home(admin_server):
    """test home endpoint"""
    resp = requests.get("http://127.0.0.1:5000/home")
    assert resp.status_code == 200
    assert resp.json() == {"hello": "world"}
