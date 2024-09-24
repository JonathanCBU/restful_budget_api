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

### The `__app__.py`

1. Make a file `restful_budget_api/__app__.py` and give it a docstring.

2. Add these imports:

    ```python
    from flask import Flask
    from flask_restful import Api
    import argparse
    import dotenv
    ```

    - Flask and Api are the objects at the core of this project
    - argparse allows us to parse command line arguments to our Poetry entry point
    - dotenv will read the .env file we wrote in [step 1](./step_1.md#the-env-file)

3. Define four functions:
    
    - `main() -> None` to run the app from the entry point (no parameters, no returns).
    - `create_app(database: str) -> Flask` to create the actual app.
    - `create_api(app: Flask) -> Api` for creating an api object and adding endpoints.
    - `get_args() -> argparse.Namespace` to handle command line args.
        - command line args should be:
            - debug: bool - launches app in debug mode (defaults to False)
            - host: string - host IP (defaults to None)
            - port: int - port to run app on (defaults to None)

4. Remember to give your functions docstrings. Because I like to type-hint everything I don't explicitly mention types in my docstrings, though I do explain each parameter and the return(s)

5. My solution:
    ```python
    def main() -> None:
        """main entrypoint for running flask server"""
        dotenv.load_dotenv()
        args = get_args()
        app = create_app(os.environ["DEMO_DB"], args.debug)
        api = create_api(app)
        for resource in api.resources:
            print(f"Added resource: {resource}")
        app.run(host=args.host, port=args.port)


    def create_app(database: str, debug: bool) -> Flask:
        """generate the Flask object without starting the server

        :param database: absolute path to your db file
        :param debug: if True, configure server for debug mode
        """
        app = Flask(__name__)
        app.config["DATABASE"] = database
        app.config["DEBUG"] = debug
        return app


    def create_api(app: Flask) -> Api:
        """create an Api and add resources with endpoints

        :param app: Flask object to build Api from
        """
        api = Api(app)
        return api


    def get_args() -> argparse.Namespace:
        """parse server CLI"""
        parser = argparse.ArgumentParser(
            description=(
                "Command line args for starting the Financify backend server"
            )
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="Enable debug mode when running the app",
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
    - create_app and create_api are both super simple and could run in the main function without issue, we need to separate creating the Flask objects and running the processes for future testing.
    - You should be able to run the app from the poetry entrypoint. From a terminal (in the root dir of the repo) run `poetry runapp --debug --port 9999`. There are no resources yes, so all you can get are 404 errors, but if you see something like the below output then we're on the right track!
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