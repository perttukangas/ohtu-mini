import os
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from src.utils.db import connect


def register(username, password):
  # ...

  hash_value = generate_password_hash(password)

  # ...

  return True

def login(username, password):
  
  # ...

  session["csrf_token"] = os.urandom(16).hex()
  return True
