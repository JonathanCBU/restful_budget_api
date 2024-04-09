from flask import Flask, jsonify
from flask import g as GlobalCtx
import dotenv
from financify_api.library.db_reader import FinancifyDb
import os

dotenv.load_dotenv()

app = Flask(__name__)


@app.before_request
def load_db():
    GlobalCtx.db = FinancifyDb(os.environ["EXAMPLE_DB"])


@app.route("/")
def api_map():
    """Return list of API endpoints"""
    return {
        "/": "This help info",
        "/table/statements": "statements table (use /table to find named tables)",
    }


@app.route("/table/statements")
def hello_em():
    table = GlobalCtx.db.get_table("statements", "date")
    return jsonify(table)
