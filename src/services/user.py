import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils.db import connect

def create_user_table():
  con = connect()

  # [IF NOT EXISTS]
  sql = "..."

  con.run(sql)

  # Muista sulkea tietokantayhteys kyselyjen jälkeen!
  con.close()
  # ...


def register(username, password):
  # ...

  hash_value = generate_password_hash(password)

  # ...

  return True

def login(username, password):
  
  # ...

  session["csrf_token"] = os.urandom(16).hex()
  return True
