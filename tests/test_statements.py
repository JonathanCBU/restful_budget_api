"""assets and liabilities endpoints testing"""

import json
from multiprocessing import Process
from typing import Dict, List, Union

import pytest
import requests

import tests.library.test_globals as test_globals


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_asset_post_and_get(
    base_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]
):
    """Assets endpoint should be able to add assets when passing a valid api key"""
    # verify posting assets
    for asset in dummy_assets:
        asset["api_key"] = "pwd1"
        resp = requests.post(
            f"{test_globals.url}/assets",
            data=json.dumps(asset),
            headers=test_globals.headers,
            timeout=5,
        )
        assert resp.status_code == 201
    get_payload = {"api_key": "pwd1"}
    resp = requests.get(f"{test_globals.url}/assets", data=json.dumps(get_payload), headers=test_globals.headers, timeout=5)

    # verify getting assets we just posted
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == 2

    # verify limiting responses to user requesting assets 

    # verify preventing access with bad api_key 

@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_liabilities_post(
    base_access_app: Process, dummy_liabilities: List[Dict[str, Union[str, float]]]
):
    """Assets endpoint should be able to add assets when passing a valid api key"""
    for liability in dummy_liabilities:
        liability["api_key"] = "pwd1"
        resp = requests.post(
            f"{test_globals.url}/liabilities",
            data=json.dumps(liability),
            headers=test_globals.headers,
            timeout=5,
        )
        assert resp.status_code == 201
