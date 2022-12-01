import os
import pg8000.dbapi

def connect():
  return pg8000.dbapi.connect(
    user=os.environ.get("DB_USERNAME"),
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_DATABASE"), 
    port=os.environ.get("DB_PORT"),
    password=os.environ.get("DB_PASSWORD"), 
    ssl_context=True
    )
