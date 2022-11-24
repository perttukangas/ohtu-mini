from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test():
    print(":)")
    return render_template("test.html")


@app.route("/pingis")
def ping():
    print("ok")
    print("yeehaaw")
    return "pongis"
