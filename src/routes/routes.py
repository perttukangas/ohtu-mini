from flask import render_template
from app import app

@app.route("/")
def index():
    print(__name__)
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/ping")
def ping():
    return "pong"
