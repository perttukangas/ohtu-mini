from flask import session
from src.utils.db import connect


def add_reference(user_id, ref_id, ref_name, columns, values):
    con = connect()
    cur = con.cursor()

    cur.execute(generate_add_sql(columns), (user_id, ref_id, ref_name) + tuple(values))

    con.commit()
    con.close()

def generate_add_sql(columns):
    column = ", ".join(columns)
    formatter = ", ".join("%s" for _ in range(len(columns)))
    return f"INSERT INTO tblReference (user_id, reference_id, reference_name, {column}) VALUES (%s, %s, %s, {formatter})"

def get_references(user_id):
    con = connect()
    cur = con.cursor()
    cur.execute(f"SELECT * FROM tblReference WHERE user_id={user_id}")
   # cur.execute("SELECT * FROM tblReference WHERE user_id=%s", (user_id,))
    filtered_results = []
    results = _get_keys_and_values(cur)
    for dict in results:
        new_dict = {}
        for (key, value) in dict.items():
            if value and not None:
                new_dict[key] = value
        filtered_results.append(new_dict)
    print(filtered_results)
    
    con.close()

    return filtered_results

def _get_keys_and_values(cursor):
    rows = cursor.fetchall()
    keys = [k[0] for k in cursor.description]
    return [dict(zip(keys, row)) for row in rows]
