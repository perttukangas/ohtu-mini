import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils.db import connect


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        query = "INSERT INTO Users (username, password) VALUES (:username, :password)"
        con = connect()
        con.run(query, username=username, password=hash_value)
        con.close()
        print("services.register done")
    except:
        con.close()
        return False
    return True

def login(username, password):
  
    query = "SELECT id, username, password FROM Users WHERE username=:username"
    con = connect()
    try:
        user = con.run(query, username=username)[0]
        con.close()
    except:
        con.close()
        print("nimeä ei löytynyt tietokannasta")
        return False
    if check_password_hash(user[2], password):
        session["user_id"] = user[0]
        session["user_username"] = user[1]
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["csrf_token"]

# TESTAAMISTA VARTEN !!!
def show_users():
    con = connect()
    for row in con.run("SELECT * FROM Users"):
        print(row)
    con.close()
