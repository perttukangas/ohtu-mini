from flask import render_template, session
from app import app
from ..services import reference
from ..utils import reference_type

@app.route("/")
def index():
    user_id = session.get("user_id", 0)
    return render_template("index.html", references=reference_type.get_references_for_index(),
        added_references=reference.get_references(user_id))


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/ping")
def ping():
    return "pong"
