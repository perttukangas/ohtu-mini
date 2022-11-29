from flask import render_template, request, redirect, session
from app import app
from ..services import user, references

@app.route("/", methods=["GET", "POST"])
def index():
    refs = []
    if session.get("user_id") is not None:
        refs = references.get_references()

    if request.method == "POST":
        ref_id = request.form["ref_id"]
        author = request.form["author"]
        heading = request.form["heading"]
        magazine = request.form["magazine"]
        year = request.form["year"]
        volume = request.form["volume"]
        doi = request.form["doi"]
        publisher = request.form["publisher"]
        pages = request.form["pages"]

        error_msg = ""
        error_msg = references.check_validation(ref_id, author, heading,
        magazine, year)

        if error_msg != "":
            return render_template("index.html", message=error_msg)
        else:
            references.add_reference(ref_id, author, heading, magazine, year,
            volume, doi, publisher, pages)

        return redirect("/")

    return render_template("index.html", references = refs), 200


@app.route("/test")
def test():
    return render_template("test.html"), 200


@app.route("/ping")
def ping():
    return "pong"
