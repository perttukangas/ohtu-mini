from flask import render_template, request, redirect
from app import app
from ..services import user


@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user.login(username, password):
            if request.referrer == "/login":
                return redirect("/")
            return redirect(request.referrer)
        return redirect("/")


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
"""
@app.route("/showall")
def showall():
    user.show_users()
    return redirect("/register")
"""
