from pg8000.exceptions import DatabaseError
from flask import render_template, request, redirect, session, abort, send_file
from collections import deque
from app import app
from ..services import reference
from ..utils import reference_type
from ..utils.reference_type import ReferenceType
from ..utils.validator import Validator

@app.route("/add/<type_name>")
def add_redirect(type_name):
    return get_add_page(type_name, "")

@app.route("/add", methods=["POST"])
def add():

    validator = Validator(request.form)

    type_name = request.form.get("reference_name")
    ref_id = request.form.get("reference_id")

    if validator.run_all_validators():
        if validator.error == "404":
            abort(404)
        return get_add_page(type_name, validator.error)

    user_id = session["user_id"]
    try:
        reference.add_reference(user_id, ref_id, type_name, validator.columns, validator.values)
    except DatabaseError:
        return get_add_page(type_name, f"ID '{ref_id}' on jo käytössä!")

    return redirect("/")

def get_add_page(reference_name, message):
    try:
        ReferenceType[reference_name]
    except KeyError:
        abort(404)

    ref_type = ReferenceType[reference_name]
    required = ref_type.get_required_for_add()
    optional = ref_type.get_optional_for_add()
    return render_template(
        "add.html",
        type=(reference_name,ref_type.get_name()),
        required=required,
        optional=optional,
        message=message
        )

@app.route("/delete", methods=["POST"])
def delete():
    selected = deque(request.form.getlist('ref_checkbox'))
    user_id = session["user_id"]
    if selected and user_id:
        selected.appendleft(user_id)
        try:
            reference.delete_selected(selected)
        except DatabaseError:
            abort(403)
    return redirect("/")

@app.route("/addbib", methods=["GET"])
def addbib():
    return render_template("addbib.html")

@app.route("/finddoi", methods=["POST"])
def find_doi():
    doi = request.form.get("doi", "")
    if len(doi) < 1:
        return render_template("addbib.html", message="Et täyttänyt DOI kenttää")

    return render_template("addbib.html", fetchedbib=reference.find_bib_by_doi(doi))

@app.route("/addbibdb", methods=["POST"])
def addbibdb():

    bib_database = reference.get_bibtex_database(request.form.get("addbib"))
    db_entries = reference.from_bibtexparser_to_db(bib_database.entries)

    for entry in db_entries:

        validator = Validator(entry)

        type_name = entry.get("reference_name")
        ref_id = entry.get("reference_id")

        if validator.run_all_validators():
            if validator.error == "404":
                abort(404)
            return render_template("addbib.html", message=validator.error)

        user_id = session["user_id"]
        try:
            reference.add_reference(user_id, ref_id, type_name, validator.columns, validator.values)
        except DatabaseError:
            return render_template("addbib.html", message=f"ID '{ref_id}' on jo käytössä!")

    return redirect("/")

@app.route("/download-file", methods=["GET"])
def file_downloads():
    user_id = session["user_id"]
    entries = reference.get_references(user_id)
    bibtex_string = reference.generate_bibtex_string(entries)
    file_obj = reference.get_bibtex_in_bytes(bibtex_string)
    return send_file(file_obj, mimetype="text/bibliography",
                    as_attachment=True, download_name="bibtex.bib")

@app.route("/download-selected", methods=["POST"])
def download_selected():
    # tämä pitää toteuttaa
    # alla olevalla saa kaikkien valituiden viitteiden id:t
    # request.form.getlist('ref_checkbox')
    return redirect("/")

@app.route("/search", methods=["POST"])
def search():
    """Suorittaa haun tekijän ja/tai vuoden mukaan.
    """

    user_id = session["user_id"]
    search_author = request.form["search_author"]
    search_year = request.form["search_year"]
    added_references = reference.get_references(user_id, search_author, search_year)

    if len(added_references) > 0:
        return render_template("index.html", references=reference_type.get_references_for_index(),
    added_references=added_references)

    else:
        msg = "Hakusi ei tuottanut tulosta. Ole hyvä ja yritä uudelleen."
        return render_template("index.html", message=msg, references=reference_type.get_references_for_index(),
    added_references=added_references)