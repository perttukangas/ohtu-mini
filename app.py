import os
import sqlparse
from flask import Flask
from src.utils.db import connect

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Tarkastetaan, että kaikki tarvittavat taulut löytyvät tietokannasta ->
# Jos pitää tehdä uusi taulu, lisää se schema.sql ja käynnistä sovellus.
def run_sql_schema():
    con = connect()
    cur = con.cursor()
    file = app.open_resource('schema.sql', 'r')
    statements = sqlparse.split(file.read())

    for statement in statements:
        #print(f"executed: {statement}")
        cur.execute(statement)

    file.close()
    con.commit()
    con.close()

run_sql_schema()


from src.routes import routes
from src.routes import user
