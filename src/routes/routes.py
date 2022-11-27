from flask import render_template, request, redirect, session
from app import app
from ..services import user, references

@app.route("/", methods=["GET", "POST"])
def index():
    refs = []
    if session.get("user_id") is not None:
        refs = references.get_references()
        references.testi_tietokantaan()
        print(refs, "viitteet")

    if request.method == "POST":
        ref_id = request.form["ref_id"]
        author = request.form["author"]
        heading = request.form["heading"]
        year = request.form["year"]
        magazine = request.form["magazine"]
        volume = request.form["volume"]
        doi = request.form["doi"]
        publisher = request.form["publisher"]
        pages = request.form["pages"]

        print(ref_id, author, heading, year, magazine)
        error_msg = ""
        error_msg = references.check_validation(ref_id, author, heading, year,
        magazine)

        if error_msg != "":
            return render_template("index.html", message=error_msg)
        else:
            references.add_reference(ref_id, author, heading, year, magazine,
            volume, doi, publisher, pages)

        references.testi_tietokantaan()
        return redirect("/")

    return render_template("index.html", references = refs), 200


@app.route("/test")
def test():
    return render_template("test.html"), 200


@app.route("/ping")
def ping():
    return "pong"
