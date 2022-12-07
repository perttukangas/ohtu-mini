from pg8000.exceptions import DatabaseError
from flask import render_template, request, redirect, session, abort, send_file
from app import app
from ..services import reference
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

@app.route("/download-file", methods=["GET"])
def file_downloads():
    user_id = session["user_id"]
    entries = reference.get_references(user_id)
    bibtex_string = reference.generate_bibtex_string(entries)
    file_obj = reference.get_bibtex_in_bytes(bibtex_string)
    return send_file(file_obj, mimetype="text/bibliography", as_attachment=True, download_name="bibtex.bib")
