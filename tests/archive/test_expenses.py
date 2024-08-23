"""expenses and liabilities endpoints testing"""

import json
from multiprocessing import Process
from typing import Dict, List, Union

import requests

from tests.library import test_globals
from tests.library.db_setup import insert_test_users


def test_expense_resource_success(
    base_access_app: Process,
    dummy_expenses: List[Dict[str, Union[str, float]]],
) -> None:
    """Assets endpoint should be able to add expenses when passing a valid api
    key
    """
    # verify posting expenses
    insert_test_users(base_access_app["db"])
    for expense in dummy_expenses:
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/expenses",
            data=json.dumps(expense),
            headers={
                "Authorization": "pwd1",
                "Content-Type": "application/json",
            },
            timeout=5,
        )
        assert resp.status_code == 201
        resp_json = resp.json()
        assert resp_json["date"] == expense["date"]
        assert resp_json["description"] == expense["description"]
        assert resp_json["amount"] == expense["amount"]
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/expenses",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )

    # verify getting expenses we just posted
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == len(dummy_expenses)

    # verify exact contents of first record
    record_0 = resp.json()[0]
    assert record_0["date"] == dummy_expenses[0]["date"]
    assert record_0["description"] == dummy_expenses[0]["description"]
    assert record_0["amount"] == dummy_expenses[0]["amount"]
    assert record_0["id"] == 1

    # verify limiting responses to user requesting expenses
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/expenses",
        headers={"Authorization": "pwd2"},
        timeout=5,
    )
    assert resp.json() == []

    # verify delete verb
    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/expenses/1",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert resp.status_code == 200
    expenses = requests.get(
        f"{test_globals.DEFAULT_URL}/expenses",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert len(expenses.json()) == len(dummy_expenses) - 1
    record_0 = expenses.json()[0]
    assert record_0["id"] == 2
    assert record_0["date"] == dummy_expenses[1]["date"]
    assert record_0["description"] == dummy_expenses[1]["description"]
    assert record_0["amount"] == dummy_expenses[1]["amount"]


def test_expense_resource_errors(
    base_access_app: Process,
    dummy_expenses: List[Dict[str, Union[str, float]]],
) -> None:
    """Assets endpoint should be able to add expenses when passing a valid api
    key"""
    insert_test_users(base_access_app["db"])
    # post expenses for testing
    for expense in dummy_expenses:
        resp = requests.post(
            f"{test_globals.DEFAULT_URL}/expenses",
            data=json.dumps(expense),
            headers={
                "Authorization": "pwd1",
                "Content-Type": "application/json",
            },
            timeout=5,
        )

    # verify get behavior with bad api_key
    resp = requests.get(
        f"{test_globals.DEFAULT_URL}/expenses",
        headers={"Authorization": "wrong_password"},
        timeout=5,
    )
    assert resp.status_code == 401
    assert resp.json() == {"error": "API key not valid"}

    # verify post behavior with missing field
    expense = {"date": "2021-01", "description": "bank"}
    resp = requests.post(
        f"{test_globals.DEFAULT_URL}/expenses",
        data=json.dumps(expense),
        headers={"Authorization": "pwd1", "Content-Type": "application/json"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "field amount not provided"

    # verify delete error codes
    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/expenses/1000",
        headers={"Authorization": "pwd1"},
        timeout=5,
    )
    assert resp.status_code == 400
    assert resp.json()["error"] == "expenses id invalid"

    resp = requests.delete(
        f"{test_globals.DEFAULT_URL}/expenses/1",
        headers={"Authorization": "pwd2"},
        timeout=5,
    )
    assert resp.status_code == 403
    assert resp.json()["error"] == "no access to expenses id 1"
