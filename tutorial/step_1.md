# Step 1

## Setting up the database and .env

### The Schema file

1. Create a .sql file in your module

    ```bash
    touch <repo_root>/restful_budget_api/schema.sql
    ```

2. Open schema.sql and write in SQL to create our two tables

    ```sql
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      UNIQUE (username)
    );

    CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      date TEXT NOT NULL,
      description TEXT NOT NULL,
      amount REAL NOT NULL,
      FOREIGN KEY(user_id) REFERENCES user(id)
    );
    ```

### The DB file

1. Create the dbs directory

    ```bash
    mkdir <repo_root>/dbs
    ```

2. Launch sqlite3 and create the actual db file

    ```bash
    sqlite3 <repo_root>/dbs/demo.db
    ```

3. From your sqlite3 session, run the schema file

    ```sql
    .read <repo_root>/restful_budget_api/schema.sql
    ```

4. Create a dummy user with a ~dangerously~ simple password (will be helpful for dev later)

    ```sql
    INSERT INTO users (username, password) VALUES ("tester", "1234");
    SELECT * FROM users;
    .exit
    ```

### The Env file

1. Create a local .env with the path to your demo.db

    ```bash
    echo "DEMO_DB='${PWD}/dbs/demo.db'" > <repo_root>/.env
    ```

## Summary

1. We wrote a SQL file and used it to create an empty database with a one-to-many relationship between user records and the user_id property of expense records:

    ![image](../assets/db_schema.drawio.png)

2. We created a dummy user names tester with a password of 1234

3. We added the absolute path of our database to a .env file so Python can find the DB without a need to commit any private info from our path to the repo


## Extra Credit (Do this all programmatically)

### DIY 

Add a setup poetry script that:

1. Is callable from the command line by prepending `poetry run`
2. Creates a .env file with the DEMO_DB variable
3. Sets up the users and expenses tables using the schema.sql file

### My Solution

1. Add this to your pyproject.toml under [tool.poetry.scripts]

    ```toml
    setup = "restful_budget_api.__setup__:main"
    ```

2. Add dotenv to your tool.poetry.dependencies

    ```toml
    python-dotenv = "^1.0.1"
    ```

3. Copy the below code into <repo_root>/restful_budget_api/__setup__.py

    ```python
    """project setup endtry point"""

    import os
    import sqlite3

    import dotenv


    def main() -> None:
        """create database file"""
        env_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env"
        )
        if not os.path.exists(env_path):
            dotenv.set_key(
                dotenv_path=env_path,
                key_to_set="DEMO_DB",
                value_to_set="${PWD}/dbs/demo.db",
            )
        dotenv.load_dotenv()
        if not os.path.exists(os.path.dirname(os.environ["DEMO_DB"])):
            os.makedirs(os.path.dirname(os.environ["DEMO_DB"]))
        db_client = sqlite3.connect(os.environ["DEMO_DB"])
        with open(
            os.path.join(os.path.dirname(__file__), "schema.sql"),
            "r",
            encoding="utf-8",
        ) as schema:
            db_client.executescript(schema.read())
        db_client.close()
    ```