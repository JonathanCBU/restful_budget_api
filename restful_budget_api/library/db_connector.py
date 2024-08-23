"""API DB connection functions"""

import sqlite3
from typing import Any, Dict, List, Tuple

from flask import current_app


def db_build_record(row: sqlite3.Row) -> Dict[str, Any]:
    """create a hashmap based on table schema

    :param row: record response
    """
    record = dict.fromkeys(row.keys()) 
    for col in row:
        record[col] == row[col]
    return record

def db_build_table(
   rows: List[sqlite3.Row] 
) -> List[Dict[str, Any]]:
    """create a list of record objects

    :param table: record list response
    """
    records = []
    for row in rows:
        record = dict.fromkeys(rows[0].keys()) 
        for col in record:
            record[col] = row[col]
        records.append(record)
    return records


def db_fetchone(sql: str, data: Tuple[Any, ...] = tuple("")) -> sqlite3.Row:
    """get single record response from database

    :param sql: formatted SQL statement
    :param data: tuple of variables to insert into sql
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_client.row_factory = sqlite3.Row
    db_cur = db_client.execute(sql, data)
    fetch = db_cur.fetchone()
    db_client.close()
    if fetch is None:
        row = sqlite3.Row(db_cur, ())
    if not isinstance(fetch, sqlite3.Row):
        raise TypeError(
            f"query: {sql} and data: {data} returned a non-Row type"
        )
    else:
        row = fetch
    for r in row.keys():
        print(f"{r} : {row[r]}")
    return row


def db_fetchall(
    sql: str, data: Tuple[Any, ...] = tuple("")
) -> List[sqlite3.Row]:
    """get table or subset of table form database

    :param sql: formatted SQL statement
    :param data: tuple of variables to insert into sql
    """
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_client.row_factory = sqlite3.Row
    db_cur = db_client.execute(sql, data)
    fetch = db_cur.fetchall()
    db_client.close()
    if not fetch:
        table = [sqlite3.Row(db_cur, ())]
    if not isinstance(fetch[0], sqlite3.Row):
        raise TypeError(
            f"query: {sql} and data: {data} returned a non-Row type"
        )
    else:
        table = fetch
    return table


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
    db_client = sqlite3.connect(
        current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_client.row_factory = sqlite3.Row
    db_cur = db_client.execute(f"SELECT * FROM {table}")
    db_client.close()
    if db_cur.lastrowid is None:
        return 1
    else:
        return db_cur.lastrowid + 1

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
