from ..services import user
from flask import render_template, request, redirect
from app import app

@app.route("/login")
def login():
    # Metodin nimi pitää olla uniikki
    # Ei saa esiintyä muissakaan routeissa
    return render_template("test.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            print("väärä salasana")
        if user.register(username, password1):
            print("luotiin")
            return redirect("/")

# TÄMÄ ON VAIN TESTAAMISTA VARTEN!!!
@app.route("/showall")
def showall():
    user.show_users()
    return redirect("/register")
