# restful_budget_api

## Release Process

1. Create the release branch
    - Checkout the commit you want to base your release off of
    - Create a branch of the format `release/vMAJ.MIN.PATCH`, updating the appropriate section
2. Change the version number
    - Update the version number in `pyproject.toml`
    - Update the version number in `CHANGELOG.md` and add a new `Unreleased` section
    - Commit the version number changes
3. Push the release branch and create a PR
    - Push the release branch to the remote
    - Create a PR from the release branch to `main`
    - Add the `release` label to the PR
4. After the PR is merged, finalize the drafted release
    - Open the drafted release and change the target to "main"
    - Publish the release

## Intro

I started this project as a way to learn the basics of REST APIs and fullstack communication in general.

## Setup

### Prerequisites

1. Linux
    - I simply don't want to worry about how this works on a Windows environment, feel free to sort through the muck on your own though
2. Python Poetry (Version 1.2.0 or later)
    - Follow [these instructions](https://python-poetry.org/docs/#installing-with-the-official-installer) to install using the official Poetry installer

### Installation

1. Navigate to the root directory of the repo before running any Poetry commands (when I say root directory I mean the root of this cloned repo)
2. Install using Poetry
    - From the root directory run `poetry install`
3. Run setup entry point to configure .env and .db
    - `poetry run setup`
4. Run unit tests to make sure everything runs correctly
    - `poetry run pytest`
    - Note: I am still working out a `Max retries exceeded with url: ` error that shows up sometimes. If that happens move on to the next section.

## Running the flask server

1. Start the server in admin mode
    - `poetry run runapp --admin --debug`
    - The admin flag starts the server in the only mode that will allow it to read/write the users table
2. In a separate terminal, create a User and save the API key
    - `curl http://localhost:5000/users -v -d '{"username":"user1"}' -H "Content-Type: application/json" -X POST`
    - Will return a JSON with a password field. That's your API key so copy it somewhere for later use
3. Go ahead and stop the current flask server instance with Ctrl-C and restart without the admin flag
    - `poetry runapp --debug`
4. Optional, check that you can't create another user account when the server is not in admin mode
    - `curl http://localhost:5000/users -v -d '{"username":"user2"}' -H "Content-Type: application/json" -X POST`
5. Add some records to the db
    - `curl http://localhost:5000/expenses -v -d '{"date":"2024-01", "description":"bank", "amount":"10101.97"}' -H "Content-Type: application/json" -H "Authorization: my_key" -X POST`
    - `curl http://localhost:5000/expenses -v -d '{"date":"2024-02", "description":"one starry share", "amount":"0.097"}' -H "Content-Type: application/json" -H "Authorization: my_key" -X POST`
6. Read back the expenses for user1
    - `curl http://localhost:5000/expenses -v -H "Authorization: my_key" -X GET`

## Explanation of This Project

### Motivation

- I have used Python to request resources from REST APIs at three jobs now, but it took this project for me to fully understand what a REST API is.
- I have not directly used relational databases or query languages at past jobs so using sqlite was a solid introduction.
- This project (and hopefully others like it) are great ways for me to keep practicing writing code while in between jobs or in positions where I never have to write code.
- I love learning new things, and I find that having a tangible goal often helps me focus while working on projects. My goal with this project is to make an example of how a RESTful backend could operate for a simple web tool.

### Reasons Behind the Tech Stack

- Python is my strongest language so I knew the fastest way for me to learn REST would be via Python
- Django can whip up a simple web page very fast, but flask (and also flask_restful) are perfect for just crafting some endpoints 
- sqlite3 ships with Python so there's no setup
    - Note: I did have to intentionally open and close the db client for each query to avoid locking up sqlite3
- Believe it or not, despite 4 years in QA/test automation, I haven't used Pytest yet (normally I like to leave unit testing to devs while I get to build integrated system tests)
- Poetry and Tox are both awesome, and I try to use them for all Python projects

### My Learning Resources and Process

- [Roy Thomas Fielding's Explanation of REST](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
    - Takeways:
      - REST is a set of architecture constraints that can be satisfied in a number of ways
      - Servers do not keep track of client information between requests (stateless client-server interactions)
        - This means we need to secure user data via some other method
      - Important Vocab:
        - Resource -> intended target of an http endpoint (Database record)
        - Resource Identifier -> string or code that tells the API which resource to focus on (URL)
        - Representation -> data returned by the API relevant to a resource (JSON object)
    
- [Flask Restful Minimal API Example](https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api)
    - Takeaways:
        - Can configure endpoints so part of the endpoint is used for data processing
            - Example: expenses/1 explicitly references the asset with ID = 1
        - Resources can handle JSON data sent with the HTTP request
            - This means we have at least 2 methods for passing data to the API as part of a request

- [Flask Define and Access the Database](https://flask.palletsprojects.com/en/3.0.x/tutorial/database)
    - Takeaways:
        - Initialize .db files using the Python sqlite library and a .sql schema file
        - Flask apps can be built from mappings where we can set custom keys
            - Can use a key to set current mode for server (admin or basic)

- [SQLite Keywords](https://sqlite.org/lang.html)
    - Takeaways:
        - Similar to a lot of the SQL practice problems I did when prepping for interviews I knew I would flub
        - SQLite is the most barebones way to POC a database as far as I can tell
        - Maybe this is on me, but this was my least favorite subject under this project

- [OWASP Top 10 API Security Risks - 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10)
    - Takeaways:
        - Learning one or two endpoints for an API can help a person extrapolate the general endpoint structure. This can allow for brute force attemtps, so there must be some sort of restriction in place to limit API access.
        - The method I came up with for limiting access is requring an API key added to JSON data as part of a request
            - Note: This could be unsafe if using the API from a publicly accessible website, as somebody could just inspect network requests and see what API key is being passed from the browser to the server.
        - All your endpoints can be sent all HTTP verbs as requests, so you need to account for POSTs being hit against your GET-only endpoints.
        - Don't try to come up with some complex security process, just follow the [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

