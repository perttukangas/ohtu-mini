import os
from src.utils import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def create_user():
  sql = """
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
  )
  """
  # execute ...


def register(username, password):
  hash_value = generate_password_hash(password)

  # ...
  # True = onnistui

  return True

def login(username, password):
  sql = "SELECT id, password, role FROM users WHERE username=:username"
  result = db.session.execute(sql, {"username": username})

  # ...
  # True = onnistui

  session["csrf_token"] = os.urandom(16).hex()
  return True
