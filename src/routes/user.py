from flask import render_template, request, redirect
from app import app
from ..services import user


@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if user.login(username, password):
        return redirect("/")
    return render_template(
        "index.html", message="Käyttäjätunnus tai salasana virheellinen"
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        error_msg = validate_credentials(username, password1, password2)

        if error_msg != "":
            return render_template("index.html", message=error_msg)

        if user.register(username, password1):
            return redirect("/")
        return render_template(
            "index.html",
            message="Yhteys palvelimeen katkesi - yritä uudelleen hetken kuluttua",
        )

    return redirect("/")


def validate_credentials(username, password1, password2):
    error_msg = ""
    if user.check_user_exists(username):
        error_msg = f"Käyttätunnus '{username}' on jo käytössä"
    elif password1 != password2:
        error_msg = "Salasanat eivät täsmää"
    elif len(password1) > 30 or len(password1) < 8:
        error_msg = "Salasanan tulee olla 8-30 merkkiä pitkä"
    elif len(username) > 20 or len(username) < 3:
        error_msg = "Käyttäjätunnuksen tulee olla 3-20 merkkiä pitkä"

    return error_msg
