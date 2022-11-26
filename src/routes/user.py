from flask import render_template, request, redirect
from app import app
from ..services import user


@app.route("/logout")
def logout():
    user.logout()
    return redirect("/"), 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user.login(username, password):
            if request.referrer == "/login":
                return redirect("/"), 200
            return redirect(request.referrer), 200
    return render_template("index.html", message="Username or password incorrect"), 400


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", message="The passwords did not match"), 400
        if len(password1) > 30 or len(password1) < 8:
            return render_template(
                "register.html",
                message="The password must be between 8-30 characters long"
                ), 400
        if len(username) > 20 or len(username) < 3:
            return render_template(
                "register.html",
                message="The username must be between 3-20 characters long"
                ), 400
        if user.register(username, password1):
            print("luotiin")
            return redirect("/"), 201
    return redirect(request.referrer)

# TÄMÄ ON VAIN TESTAAMISTA VARTEN!!!

#@app.route("/showall")
#def showall():
#    user.show_users()
#    return redirect("/register")
