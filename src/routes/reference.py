from flask import render_template, request, redirect
from app import app
from ..services import reference
from ..utils import reference_type


@app.route("/add/<type_name>")
def add_redirect(type_name):
    type = reference_type.ReferenceType[type_name]
    required = type.get_required_for_add()
    optional = type.get_optional_for_add()

    print(required)
    print(optional)

    return render_template("add.html", type=(type_name, type.value[1]), required=required, optional=optional)

@app.route("/add", methods=["POST"])
def add():
    type = reference_type.ReferenceType[request.form["type_name"]]
    required = type.get_required()
    optional = type.get_optional()

    print(type)
    print(required)
    print(optional)
    data = [":)"]

    reference.add_reference(data)

    return redirect("/")


def validata_and_or():
    pass

def validate(row_type, data):
    
    # Split to separate
    if row_type == "author":
        if len(data) < 5:
            return "invalid"

    return None