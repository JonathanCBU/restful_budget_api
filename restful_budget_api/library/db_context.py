"""database controls"""

import sqlite3
import os

def make_db(db_file: str, schema_file: str = "", overwrite: bool = False) -> None:
    """execute a schema file to make a db
    
    :param db_file: absolute path to db file 
    :param schema_file: absolute path to SQL schema file (leaves db empty if null string)
    :param overwrite: deletes existing db_file if it exists
    """
    if overwrite:
        try:
            os.remove(db_file)
        except FileNotFoundError:
            print(f"Nothing to remove, {db_file} does not exits")
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    db_client = sqlite3.connect(db_file)
    if schema_file:
        with open(schema_file, "r", encoding="utf-8") as schema:
            db_client.executescript(schema.read())
    db_client.close()