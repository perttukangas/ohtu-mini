from flask import session
from src.utils.db import connect
from ..utils import reference_type

def add_reference(user_id, ref_id, ref_name, columns, values):
    print(user_id, ref_id, ref_name, columns, values)

    column = ", ".join(columns)
    formatter = ", ".join("%s" for _ in range(len(columns)))
    sql = f"INSERT INTO tblReference (user_id, reference_id, reference_name, {column}) VALUES (%s, %s, %s, {formatter})"

    print(column)
    print(formatter)
    print(sql)
    print((user_id, ref_id, ref_name) + tuple(values))

    con = connect()
    cur = con.cursor()

    cur.execute(sql, (user_id, ref_id, ref_name) + tuple(values))

    con.commit()
    con.close()

def get_references(user_id):

    print(user_id)

    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM tblReference WHERE user_id=%s", (user_id,))

    rows = cur.fetchall()
    keys = [k[0] for k in cur.description]
    results = [dict(zip(keys, row)) for row in rows]

    con.close()

    return results