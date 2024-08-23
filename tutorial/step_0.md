# Step 0

## Starting from close to scratch

Make sure you have Python Poetry version 1.2.0 or later installed and working.

### Archive almost everything

1. Create a folder named `_archive`

2. Move restful_budget_api (the directory at the root of this repo), tests, poetry.lock, pyproject.toml, .github, and tox.ini into _archive

### Make this a module

1. Make an empty folder with the same name as this repo at the top level so you have `<some path>/restful_budget_api/restful_budget_api`

2. Add a "dunder" init file

    ```bash
    echo '"""empty init"""' > restful_budget_api/__init__.py
    ```


### Add a place for tests

1. Make a tests folder at the root of this repo and add an empty dunder init to it

### Create you pyproject file

1. Add this to a pyproject.toml file at the root of the repo

    ```toml
    [tool.poetry]
    name = "restful-budget-api"
    version = "0.1.0"
    description = "A flask_restul app for learning REST"
    authors = ["Jonathan Cook <jcookbme@gmail.com>"]
    readme = "README.md"

    [tool.poetry.scripts]

    [tool.poetry.dependencies]
    python = "^3.10"

    [tool.poetry.group.dev.dependencies]
    ipython = "*"
    ```

2. Run `poetry install`

## Summary

1. We archived the whole repo so we can g0 step-by-step

2. We have restful_budget_api and tests modules with nothing but empty dunder inits in them

3. Our poetry project is configured for Python 3.10, and we have iPython as a dev dependency