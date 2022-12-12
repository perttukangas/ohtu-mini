import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils.db import connect


def register(username, password):
    hash_value = generate_password_hash(password)
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO Users (username, password) VALUES (%s, %s)", (username, hash_value)
        )
        con.commit()
        return True
    except Exception as ex:
        print(ex)
        return False
    finally:
        con.close()

def check_user_exists(username):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT id, username, password FROM Users WHERE username=%s", (username,)
        )
        user = cur.fetchone()
        if user is None:
            return False
        return user
    except Exception as ex:
        print(ex)
        return False
    finally:
        con.close()


def login(username, password):
    user = check_user_exists(username)
    if user != False:
        if check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["user_username"] = user[1]
            session["csrf_token"] = os.urandom(16).hex()
            return True
    return False

def logged_in():
    return "user_id" in session

def logout():
    try:
        del session["user_id"]
        del session["user_username"]
        del session["csrf_token"]
        return True
    except Exception as ex:
        print(ex)
        return False
