import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from src.utils.db import connect
from io import BytesIO
import requests


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


def get_references(user_id, search_author="", search_year=""):
    con = connect()
    cur = con.cursor()
    years = search_year.split("-")
    if search_author == "" and search_year == "":
        cur.execute("SELECT * FROM tblReference WHERE user_id=%s", (user_id,))

    elif len(years) == 1 and years[0] != "":
        if search_author != "" and search_year != "":
            cur.execute(
                "SELECT * FROM tblReference WHERE user_id=%s AND author ILIKE %s AND year=%s",
                (
                    user_id,
                    f"%{search_author}%",
                    years[0],
                ),
            )
        elif search_year != "":
            cur.execute(
                "SELECT * FROM tblReference WHERE user_id=%s AND year=%s",
                (
                    user_id,
                    years[0],
                ),
            )

    elif len(years) == 2:
        if len(years[1]) == 2:
            years[1] = years[0][0:2] + years[1]
        years[0] = str(int(years[0]) - 1)
        years[1] = str(int(years[1]) + 1)
        if search_author != "" and search_year != "":
            cur.execute(
                "SELECT * FROM tblReference WHERE user_id=%s AND author ILIKE %s AND year BETWEEN %s AND %s",
                (
                    user_id,
                    f"%{search_author}%",
                    years[0],
                    years[1],
                ),
            )
        else:
            cur.execute(
                "SELECT * FROM tblReference WHERE user_id=%s AND year BETWEEN %s AND %s",
                (
                    user_id,
                    years[0],
                    years[1],
                ),
            )

    else:
        cur.execute(
            "SELECT * FROM tblReference WHERE user_id=%s AND author ILIKE %s",
            (
                user_id,
                f"%{search_author}%",
            ),
        )

    results = _get_keys_and_values(cur)
    con.close()
    filtered_results = []
    for dict in results:
        new_dict = {}
        for (key, value) in dict.items():
            if value and not None:
                new_dict[key] = value
        filtered_results.append(new_dict)
    return filtered_results


def get_selected(entries, id_list):
    filtered_results = []
    for entry in entries:
        if str(entry["id"]) in id_list:
            filtered_results.append(entry)
    return filtered_results


def delete_selected(ids: list):
    con = connect()
    cur = con.cursor()
    n = len(ids) - 1
    # lisätään sql-kyselyyn tarpeeksi monta kertaa %s
    query = "DELETE FROM tblReference WHERE user_id=%s AND id IN ({})".format(
        ",".join(["%s"] * n)
    )
    cur.execute(query, (ids))
    con.commit()
    con.close()


def generate_bibtex_string(entries):
    db = BibDatabase()
    db.entries = from_db_to_bibtexparser(entries)

    writer = BibTexWriter()
    return writer.write(db)


def get_bibtex_in_bytes(bibtex_string):
    return BytesIO(bibtex_string.encode())


def from_db_to_bibtexparser(entries):
    for dict in entries:
        dict["ENTRYTYPE"] = dict["reference_name"].lower()
        dict["ID"] = dict["reference_id"]
        del dict["reference_name"]
        del dict["reference_id"]
        del dict["id"]
        del dict["user_id"]

    return entries


def from_bibtexparser_to_db(entries):
    for dict in entries:
        dict["reference_name"] = dict["ENTRYTYPE"].upper()
        dict["reference_id"] = dict["ID"]
        del dict["ENTRYTYPE"]
        del dict["ID"]

    return entries


def get_bibtex_database(data):
    return bibtexparser.loads(data)


def find_bib_by_doi(doi):
    response = requests.get(
        f"http://dx.doi.org/{doi}",
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
            "Accept": "text/bibliography; style=bibtex"
        },
    )

    # https://stackoverflow.com/questions/44203397/python-requests-get-returns-improperly-decoded-text-instead-of-utf-8
    # :)
    response.encoding = response.apparent_encoding

    if response.status_code != 200:
        if "Not Found" in response.text:
            return f"DOI: {doi} ei löytynyt"
        print(response.text)
        return f"Jotain meni pieleen: {response}"

    # Muuta string parempaan muotoon
    bib_database = bibtexparser.loads(response.text)
    return bibtexparser.dumps(bib_database)


def _get_keys_and_values(cursor):
    rows = cursor.fetchall()
    keys = [k[0] for k in cursor.description]
    return [dict(zip(keys, row)) for row in rows]
