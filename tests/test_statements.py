"""assets and liabilities endpoints testing"""

# pylint: disable=unused-argument

import json
from multiprocessing import Process
from typing import Dict, List, Union

import pytest
import requests

from tests.library import test_globals


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_asset_post_and_get(
    base_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]
):
    """Assets endpoint should be able to add assets when passing a valid api key"""
    # verify posting assets
    for asset in dummy_assets:
        asset["api_key"] = "pwd1"
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/assets",
            data=json.dumps(asset),
            headers=test_globals.HEADERS,
            timeout=5,
        )
        assert resp.status_code == 201
    get_payload = {"api_key": "pwd1"}
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        data=json.dumps(get_payload),
        headers=test_globals.HEADERS,
        timeout=5,
    )

    # verify getting assets we just posted
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == len(dummy_assets)

    # verify limiting responses to user requesting assets
    get_payload = {"api_key": "pwd2"}
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        data=json.dumps(get_payload),
        headers=test_globals.HEADERS,
        timeout=5,
    )
    assert resp.json() == []

    # verify preventing access with bad api_key
    get_payload = {"api_key": "wrong_password"}
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        data=json.dumps(get_payload),
        headers=test_globals.HEADERS,
        timeout=5,
    )
    assert resp.status_code == 401
    assert resp.json() == {"error": "API key not valid"}
