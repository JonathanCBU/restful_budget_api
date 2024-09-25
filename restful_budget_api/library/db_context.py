"""database controls"""

import sqlite3
import os

def make_db(db_file: str, schema_file: str = "") -> None:
    """execute a schema file to make a db
    
    :param db_file: absolute path to db file 
    :param schema_file: absolute path to SQL schema file (leaves db empty if null string)
    """
    if not os.path.exists(os.path.dirname(db_file)):
        os.makedirs(os.path.dirname(db_file))
    db_client = sqlite3.connect(db_file)
    if schema_file:
        with open(schema_file, "r", encoding="utf-8") as schema:
            db_client.executescript(schema.read())
    db_client.close()