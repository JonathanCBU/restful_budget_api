from flask import Flask, render_template
from flask import g as GlobalCtx
import dotenv
from financify_api.library.db_reader import FinancifyDb
import os

dotenv.load_dotenv()

app = Flask(__name__)


@app.before_request
def load_db():
    db = FinancifyDb(os.environ["EXAMPLE_DB"])
    GlobalCtx.db_table = db.get_table("statements", "date")


@app.route("/")
def hello_em():
    # return "<p>Hello there Em!!! :)</p>"

    return render_template("example.html", db_table=GlobalCtx.db_table)
