# financify_api

## Intro

I started this project as a way to learn the basics of REST APIs and fullstack communication in general.

## Setup

### Prerequisites

1. Linux
    - I simply don't want to worry about how this works on a Windows environment, feel free to sort through the muck on your own though
2. Python Poetry
    - Follow [these instructions](https://python-poetry.org/docs/#installing-with-the-official-installer) to install using the official Poetry installer

### Installation

1. Install using Poetry
    - From the root directory run `poetry install`
2. Setup you .env file
    - In the root directory create a .env file and add your secret env vars to it: `vim .env`
    - If you just want to use the demo database just add `DEMO_DB=${HOME}/dbs/demo.db`
    - Save you env file and exit vim by reading [this entire article about how to exit vim](https://builtin.com/articles/how-to-exit-vim)
3. Run the db_init entry point to create the demo database
    - TODO

## Features

### Security

1. OWASP recommended REST API securoty measures
    - I try to follow [OWASP's recommendations](https://owasp.org/API-Security/editions/2023/en/0x00-header/) for API security
    - Admin-only user reading and writing
    - api keys generated for each user
    - users are restricted to specific database records via their key
2. Python dotenv library
    - Envionment variables can be stored in the `.env` file and accessed using the dotenv library
    - `.env` is in the gitignore to keep it out of version control

### Testing

1. Tox
    - Tox is used to spin small virtual environments for testing
    - Black, isort, pylint, and mypy are used to enforce formatting, linting, and type-hinting in my Python code
2. Pytest
    - TODO