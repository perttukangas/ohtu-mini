from flask import render_template
from app import app

@app.route("/login")
def login():
    # Metodin nimi pitää olla uniikki
    # Ei saa esiintyä muissakaan routeissa
    return render_template("test.html")
