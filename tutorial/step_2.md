# Step 2

## Setup Flask app

### Dependencies

For our app we need Flask and Flask_restful. Add these to your pyproject.toml tool.poetry.dependencies:

```toml
flask = "^3.0.2"
flask-restful = "^0.3.10"
```

If you haven't yet, add `python-dotenv = "^1.0.1"` as well.

We also will want a poetry entry point to run the app from. Under tool.poetry.scripts add `runapp = "restful_budget_api.__app__:main"`.


### Config classes

1. Make a library directory in the module directory (`restful_budget_api/restful_budget_api/library`) and create a `configs.py` file.

2. We are going to use the `from_object` configuration method described [here](https://flask.palletsprojects.com/en/3.0.x/config/#development-production), so start with a simple set of Default and Dev classes

    ```python
    import os
    import dotenv
    
    dotenv.load_dotenv()

    class Default:
        TESTING = False
        DEBUG = False
        DATABASE = os.environ["DEMO_DB"]

    class Dev(Default):
        DEBUG = True
    ```

### The `__app__.py`

1. Make a file `restful_budget_api/__app__.py` and give it a docstring.

2. Add these imports:

    ```python
    from flask import Flask
    from flask_restful import Api
    import argparse
    import restful_budget_api.library.configs as configs
    ```

    - Flask and Api are the objects at the core of this project
    - argparse allows us to parse command line arguments to our Poetry entry point
    - configs will allow us to use the config classes in the last step

3. Define two functions:
    
    - `main() -> None` to run the app from the entry point (no parameters, no returns).
    - `get_args() -> argparse.Namespace` to handle command line args.
        - command line args should be:
            - config: string - the name of the config class to use
            - host: string - host IP (defaults to None)
            - port: int - port to run app on (defaults to None)

4. Remember to give your functions docstrings. Because I like to type-hint everything I don't explicitly mention types in my docstrings, though I do explain each parameter and the return(s)

5. My solution:
    ```python
    def main() -> None:
        """main entrypoint for running flask server"""
        args = get_args()
        app = Flask(__name__)
        app.config.from_object(getattr(configs, args.config))
        api = Api(app)
        for resource in api.resources:
            print(f"Added resource: {resource}")
        app.run(host=args.host, port=args.port)


    def get_args() -> argparse.Namespace:
        """parse server CLI"""
        parser = argparse.ArgumentParser(
            description=(
                "Command line args for starting the Financify backend server"
            )
        )
        parser.add_argument(
            "--config",
            default="Default",
            help="Specify server config",
        )
        parser.add_argument(
            "--host",
            default=None,
            help="Specify server host. Will default to localhost if left None",
        )
        parser.add_argument("--port", default=None, help="Specify server port")
        args = parser.parse_args()
        return args
    ```

6. Notes:

    - Using any host that isn't localhost exposes the flask app to your entire local network. This is fine as long as you don't put any actually sensetive information in the db.
    - You should be able to run the app from the poetry entrypoint. From a terminal (in the root dir of the repo) run `poetry runapp --config Dev --port 9999`. There are no resources so all you can get are 404 errors, but if you see something like the below output then we're on the right track!
        ```bash
            * Serving Flask app 'restful_budget_api.__app__'
            * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
            * Running on http://127.0.0.1:9999
        Press CTRL+C to quit
            * Restarting with stat
            * Debugger is active!
            * Debugger PIN: 123-429-260
        ```