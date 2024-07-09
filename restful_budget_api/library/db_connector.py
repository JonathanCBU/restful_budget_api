"""API DB connection functions"""

import sqlite3
from typing import Any, Dict, List, Tuple, Union, cast

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


def db_fetchone(sql: str, data: Tuple[Any, ...] = tuple("")) -> Union[Tuple[Any], None]:
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
    db_client.close()
    if fetch is None:
        return None
    return tuple(fetch)


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
    if fetch is not None:
        fetch = cast(Tuple[str, int], fetch)
        return int(fetch[1] + 1)
    return 1


def db_ids(table: str) -> List[int]:
    """return list of ids within table

    :param table: table name
    """
    fetch = db_fetchall(f"SELECT id FROM {table}")
    return [int(record[0]) for record in fetch]


def db_add_new_record(table: str, insert: Dict[str, Any]) -> Dict[str, Any]:
    """create a new record based on table schema and json from request

    :param table: table name
    :param insert:
    """
    record_id = db_next_id(table)
    db_commit_change(
        sql=f"INSERT INTO {table} "
        f"({', '.join(insert.keys())}) "
        f"VALUES ({', '.join(['?' for _ in insert])})",
        data=tuple(insert.values()),
    )
    fetch = db_fetchone(
        sql=f"SELECT * FROM {table} WHERE id = ?",
        data=(record_id,),
    )
    return db_build_record(fetch=fetch, schema=db_get_schema(table))
