from flask import render_template, request, redirect, session
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

    return render_template("add.html", type=(type_name, type.get_name()), required=required, optional=optional)

@app.route("/add", methods=["POST"])
def add():
    ref_type = reference_type.ReferenceType[request.form["type_name"]]
    required = ref_type.get_required()
    optional = ref_type.get_optional()

    print(ref_type)
    print(required)
    print(optional)

    columns = []
    values = []

    for req in required:
        form_data = None
        form_req = None
        if type(req) is tuple:
            both_used = validata_or(request.form[req[0]], request.form[req[1]])
            if both_used is not None:
                print(both_used)
                return redirect("/")

            form_data = request.form[req[0]] if len(request.form[req[0]]) > 0 else request.form[req[1]]
            form_req = req[0] if len(request.form[req[0]]) > 0 else req[1]
        else:
            form_data = request.form[req]
            form_req = req 
        
        if len(form_data) < 1:
            print(f"Required: {req}")
            return redirect("/")
        
        error = validate(form_req, form_data)
        if error is not None:
            print(error)
            return redirect("/")

        columns.append(form_req)
        values.append(form_data)
    
    for opt in optional:
        form_data = None
        form_opt = None
        if type(opt) is tuple:
            both_used = validata_or(request.form[opt[0]], request.form[opt[1]])
            if both_used is not None:
                print(both_used)
                return redirect("/")

            form_data = request.form[opt[0]] if len(request.form[opt[0]]) > 0 else request.form[opt[1]]
            form_opt = opt[0] if len(request.form[opt[0]]) > 0 else opt[1]
        else:
            form_data = request.form[opt]
            form_opt = opt
        
        if len(form_data) > 0:
            error = validate(form_opt, form_data)
            if error is not None:
                print(error)
                return redirect("/")
        
            columns.append(form_opt)
            values.append(form_data)


    user_id = session["user_id"]
    ref_id = request.form["reference_id"]
    ref_name = ref_type.name

    reference.add_reference(user_id, ref_id, ref_name, columns, values)

    return redirect("/")


def validata_or(form1, form2):
    return f"Vain toinen kentistä {form1} ja {form2} voi sisältää tietoa" if len(form1) > 0 and len(form2) > 0 else None

def validate(row_type, data):
    
    # Split to separate
    #if row_type == "author":
    #    if len(data) < 5:
    #        return "invalid"

    return None