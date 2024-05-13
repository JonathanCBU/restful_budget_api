"""assets and liabilities endpoints testing"""

import json
from multiprocessing import Process
from typing import Dict, List, Union

import pytest
import requests

import tests.library.test_globals as test_globals


@pytest.mark.parametrize("admin_access_app", ["users_schema"], indirect=True)
def test_asset_post(
    admin_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]
):
    """Assets endpoint should be able to add assets when passing a valid api key"""
    for asset in dummy_assets:
        asset["api_key"] = "pwd1"
        resp = requests.post(
            f"{test_globals.url}/assets",
            data=json.dumps(asset),
            headers=test_globals.headers,
            timeout=5,
        )
        assert resp.status_code == 201
