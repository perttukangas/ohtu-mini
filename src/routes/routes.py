from flask import render_template
from app import app
from ..services import reference
from ..utils import reference_type

@app.route("/")
def index():
    return render_template("index.html", references=reference_type.get_references_for_index())


@app.route("/test")
def test():
    return render_template("test.html"),


@app.route("/ping")
def ping():
    return "pong"
