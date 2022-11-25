import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils.db import connect


def register(username, password):

    hash_value = generate_password_hash(password)
    try:
        query = "INSERT INTO Users (username, password) VALUES (:username,:password)"
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
    #result = 

    session["csrf_token"] = os.urandom(16).hex()
    return True

# TESTAAMISTA VARTEN !!!
def show_users():
    con = connect()
    for row in con.run("SELECT * FROM Users"):
        print(row)
    con.close()