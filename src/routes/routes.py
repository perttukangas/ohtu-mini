from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/test")
def test():
    return render_template("test.html"), 200


@app.route("/ping")
def ping():
    return "pong"
