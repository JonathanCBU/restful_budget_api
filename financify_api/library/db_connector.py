"""API DB connection functions"""

import sqlite3
from typing import Any, Dict, List, Tuple, cast

from flask import current_app


def db_get_schema(table: str) -> List[str]:
    """get table field names

    :param table: table name
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    if not isinstance(db_client, sqlite3.Connection):
        raise LookupError("Could not connect to database")
    fetch = db_client.execute(f"SELECT * FROM {table}")
    db_client.close()
    return [field[0] for field in fetch.description]


def db_build_record(fetch: Tuple[Any], schema: List[str]) -> Dict[str, Any]:
    """create a hashmap based on table schema

    :param fetch: record response
    :param schema: table field names
    """
    record = {}
    for key, val in zip(schema, fetch):
        record[key] = val
    return record


def db_build_table(fetch: List[Tuple[Any]], schema: List[str]) -> List[Dict[str, Any]]:
    """create a list of record objects

    :param fetch: record list response
    :param schema: table field names
    """
    records = []
    for row in fetch:
        record = {}
        for key, val in zip(schema, row):
            record[key] = val
        records.append(record)
    return records


def db_fetchone(sql: str, data: Tuple[Any, ...] = tuple("")) -> Tuple[Any]:
    """get single record response from database

    :param sql: formatted SQL statement
    :param data: tuple of variables to insert into sql
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    if not isinstance(db_client, sqlite3.Connection):
        raise LookupError("Could not connect to database")
    fetch = db_client.execute(sql, data).fetchone()
    print("fetch", fetch)
    print("sql", sql)
    print("params", data)
    db_client.close()
    if fetch:
        return tuple(fetch)
    return ()


def db_fetchall(sql: str, data: Tuple[Any, ...] = tuple("")) -> List[Tuple[Any]]:
    """get table or subset of table form database

    :param sql: formatted SQL statement
    :param data: tuple of variables to insert into sql
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    if not isinstance(db_client, sqlite3.Connection):
        raise LookupError("Could not connect to database")
    fetch = db_client.execute(sql, data).fetchall()
    db_client.close()
    return fetch


def db_commit_change(sql: str, data: Tuple[Any, ...] = tuple("")) -> None:
    """perform a database action without an expected response

    :param sql: formatted SQL statement
    :param data: tuple of variables to insert into sql
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    if not isinstance(db_client, sqlite3.Connection):
        raise LookupError("Could not connect to database")
    db_client.execute(sql, data)
    db_client.commit()
    db_client.close()


def db_next_id(table: str) -> int:
    """get next id number for a given table

    :param table: table name
    """
    fetch = db_fetchone(f"SELECT * FROM SQLITE_SEQUENCE WHERE name='{table}'")
    if len(fetch) == 2:
        fetch = cast(Tuple[str, int], fetch)
        return int(fetch[1] + 1)
    return 1


def db_ids(table: str) -> List[int]:
    """return list of ids within table

    :param table: table name
    """
    fetch = db_fetchall(f"SELECT id FROM {table}")
    return [int(record[0]) for record in fetch]
