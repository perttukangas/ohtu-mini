import os
import pg8000.native

# Connect to the database with user name postgres

print(os.environ.get("DB_USERNAME"))
print(os.environ.get("DB_HOST"))
print(os.environ.get("DB_DATABASE"))
print(os.environ.get("DB_PORT"))
print(os.environ.get("DB_PASSWORD"))

con = pg8000.native.Connection(os.environ.get("DB_USERNAME"),
  host=os.environ.get("DB_HOST"),
  database=os.environ.get("DB_DATABASE"), 
  port=os.environ.get("DB_PORT"),
  password=os.environ.get("DB_PASSWORD"), 
  ssl_context=True
  )

# Create a temporary table
con.run("CREATE TABLE book (id SERIAL, title TEXT)")

# Populate the table
for title in ("Ender's Game", "The Magus"):
  con.run("INSERT INTO book (title) VALUES (:title)", title=title)

# Print all the rows in the table
for row in con.run("SELECT * FROM book"):
  print(row)
#[1, "Ender's Game"]
#[2, 'The Magus']

con.close()