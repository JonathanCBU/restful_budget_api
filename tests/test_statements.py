"""assets and liabilities endpoints testing"""

# pylint: disable=unused-argument

import json
from multiprocessing import Process
from typing import Dict, List, Union

import pytest
import requests

from tests.library import test_globals


@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_asset_resource_success(
    base_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]
) -> None:
    """Assets endpoint should be able to add assets when passing a valid api key"""
    # verify posting assets
    for asset in dummy_assets:
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/assets",
            data=json.dumps(asset),
            headers={"Authorization": "pwd1", "Content-Type": "application/json"},
            timeout=5,
        )
        assert resp.status_code == 201
        resp_json = resp.json()
        assert resp_json["date"] == asset["date"]
        assert resp_json["description"] == asset["description"]
        assert resp_json["value"] == asset["value"]
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )

    # verify getting assets we just posted
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == len(dummy_assets)

    # verify exact contents of first record
    record_0 = resp.json()[0]
    assert record_0["date"] == dummy_assets[0]["date"]
    assert record_0["description"] == dummy_assets[0]["description"]
    assert record_0["value"] == dummy_assets[0]["value"]
    assert record_0["id"] == 1

    # verify limiting responses to user requesting assets
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "pwd2"},
        timeout=5,
    )
    assert resp.json() == []  

    # verify patch to update asset report_id
    get_payload = {"report_id": 2}
    resp = requests.patch(
        f"{test_globals.DEFAULT_URL}/assets/1",
        data=json.dumps(get_payload),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 200
    assets = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    record_0 = assets.json()[0]
    assert record_0["report_id"] == 2
    assert record_0["id"] == 1
    assert record_0["date"] == dummy_assets[0]["date"]
    assert record_0["description"] == dummy_assets[0]["description"]
    assert record_0["value"] == dummy_assets[0]["value"]

    # verify delete verb
    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/assets/1",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert resp.status_code == 200
    assets = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert len(assets.json()) == len(dummy_assets) - 1
    record_0 = assets.json()[0]
    assert record_0["id"] == 2
    assert record_0["date"] == dummy_assets[1]["date"]
    assert record_0["description"] == dummy_assets[1]["description"]
    assert record_0["value"] == dummy_assets[1]["value"]

@pytest.mark.parametrize("base_access_app", ["users_schema"], indirect=True)
def test_asset_resource_errors(
    base_access_app: Process, dummy_assets: List[Dict[str, Union[str, float]]]
) -> None:
    """Assets endpoint should be able to add assets when passing a valid api key"""
    # post assets for testing
    for asset in dummy_assets:
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/assets",
            data=json.dumps(asset),
            headers={"Authorization": "pwd1", "Content-Type": "application/json"},
            timeout=5,
        )

    # verify get behavior with bad api_key
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/assets",
        headers={"Authorization": "wrong_password"},
        timeout=5,
    )
    assert resp.status_code == 401
    assert resp.json() == {"error": "API key not valid"}

    # verify post behavior with missing field
    asset = {"date": "2021-01", "description": "bank"}
    resp = requests.post(
        f"{test_globals.DEFAULT_URL}/assets",
        data=json.dumps(asset),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "field value not provided"

    # verify delete error codes
    get_payload = {"api_key": "pwd1"}
    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/assets/1000",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "assets id invalid"

    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/assets/1",
        headers={"Authorization": "pwd2"},
        timeout=5,
    )
    assert resp.status_code == 403
    assert resp.json()["error"] == "no access to assets id 1"

    # verify patch error codes
    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/assets/1000",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "assets id invalid"

    get_payload = {"report_id": 2}
    resp = requests.patch(
        f"{test_globals.DEFAULT_URL}/reports/1",
        data=json.dumps(get_payload),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 405
    assert resp.json()["error"] == "reports does not have a patch method"

    resp = requests.patch(
        f"{test_globals.DEFAULT_URL}/assets/1000",
        data=json.dumps(get_payload),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "assets id invalid"

    get_payload = {"report_id": 2}
    resp = requests.patch(
        f"{test_globals.DEFAULT_URL}/assets/1",
        data=json.dumps(get_payload),
        headers={"Authorization": "pwd2", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 403
    assert resp.json()["error"] == "no access to assets id 1"

    get_payload = {"placeholder": "Silly"}
    resp = requests.patch(
        f"{test_globals.DEFAULT_URL}/assets/1",
        data=json.dumps(get_payload),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "field report_id not provided"
