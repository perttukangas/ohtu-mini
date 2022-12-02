from flask import render_template, request, redirect, session
from app import app
from ..services import reference
from ..utils import reference_type


@app.route("/add/<type_name>")
def add_redirect(type_name):
    return get_add_page(type_name, "")

@app.route("/add", methods=["POST"])
def add():
    ref_type = reference_type.ReferenceType[request.form["type_name"]]
    required = ref_type.get_required()
    optional = ref_type.get_optional()

    columns = []
    values = []

    ref_name = ref_type.name

    required_validation = validate_input(ref_name, required, columns, values, True)
    if required_validation is not None:
        return required_validation
    
    optional_validation = validate_input(ref_name, optional, columns, values, False)
    if optional_validation is not None:
        return optional_validation

    user_id = session["user_id"]
    ref_id = request.form["reference_id"]

    reference.add_reference(user_id, ref_id, ref_name, columns, values)

    return redirect("/")

def get_add_page(type_name, message):
    type = reference_type.ReferenceType[type_name]
    required = type.get_required_for_add()
    optional = type.get_optional_for_add()
    return render_template("add.html", type=(type_name, type.get_name()), required=required, optional=optional, message=message)

def validate_input(ref_type, types, columns, values, required):
    for cur_type in types:

        form_resp = get_form_data(cur_type)
        if len(form_resp) != 2:
            return get_add_page(ref_type, form_resp)
        
        form_type, form_data = form_resp
        
        if len(form_data) < 1 and required:
            return get_add_page(ref_type, f"Vaadittu kenttä täyttämättä: {cur_type}")
        
        error = validate(form_type, form_data)
        if error is not None:
            return get_add_page(ref_type, error)

        columns.append(form_type)
        values.append(form_data)

def get_form_data(cur_type):
    if type(cur_type) is tuple:
        if len(request.form[cur_type[0]]) > 0 and len(request.form[cur_type[1]]) > 0:
            return f"Vain toinen kentistä {cur_type[0]} ja {cur_type[1]} voi sisältää tietoa"

        form_type = cur_type[0] if len(request.form[cur_type[0]]) > 0 else cur_type[1]
        form_data = request.form[form_type]
    else:
        form_type = cur_type 
        form_data = request.form[cur_type]
    return (form_type, form_data)

def validate(row_type, data):
    
    # Split to separate
    #if row_type == "author":
    #    if len(data) < 5:
    #        return "invalid"

    return None