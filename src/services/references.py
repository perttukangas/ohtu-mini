import os
from flask import session
from src.utils.db import connect

#pakolliset artikkeliin: id, tekijä, otsikko, julkaisuvuosi, lehden nimi
#vapaavalintainen: volyymi ja numero, artikkelin tunniste, julkaisija, sivut.

def add_reference(ref_id, author, heading, year, magazine):
    """Funktio lisää artikkeliviitteen tiedot tietokantaan.
    """

    user_id = int(session.get("user_id"))
    query = "INSERT INTO Article_Ref (ref_id, user_id, author, heading, year, magazine) VALUES (:ref_id, :user_id, :author, :heading, :year, :magazine)"
    con = connect()

    try:
        con.run(query, ref_id=ref_id, user_id=user_id, author=author, heading=heading, year=year, magazine=magazine)
        con.close()
    except:
        con.close()
        print("fail")
        return False
    return True

def check_validation(ref_id, author, heading, year, magazine):
    """Funktiossa tarkistetaan onko HTML-lomakkeessa annetut pakolliset tiedot
    täytetty ehtojen mukaisesti. Mikäli ei ole, palautetaan virheilmoitus.
    """

    error_msg = ""

    if len(ref_id) < 2 or len(ref_id) > 50:
        error_msg = "ID-tunnus on liian lyhyt tai liian pitkä"
    if len(author) < 2 or len(author) > 300:
        error_msg = "Tekijän nimi/nimet ovat liian lyhyet tai liian pitkät"
    if len(heading) < 2 or len(heading) > 200:
        error_msg = "Otsikko on liian lyhyt tai liian pitkä"
    if len(year) != 4:
        error_msg = "Vuosiluku annettu väärin"
    if len(magazine) < 2 or len(magazine) > 200:
        error_msg = "Lehden nimi on liian lyhyt tai liian pitkä"

    user_id = int(session.get("user_id"))
    query2 = "SELECT ref_id FROM Article_Ref WHERE user_id=:user_id AND ref_id=:ref_id"
    con = connect()
    unique_id = con.run(query2, ref_id=ref_id, user_id=user_id)
    con.close()
    if unique_id != []:
        error_msg = "ID-tunnus on jo käytössä. Kokeile toista."

    return error_msg

def get_references():
    """"Funktio hakee listan viitteistä kirjautuneen käyttäjän id:n perusteella
    """

    user_id = int(session.get("user_id"))
    query = "SELECT author, heading, year, magazine FROM Article_Ref WHERE user_id=:user_id"
    con = connect()

    try:
        ref_list = con.run(query, user_id=user_id)
        con.close()
        return ref_list
    except:
        con.close()
        print("toinen fail")
        return False

def testi_tietokantaan():
    con = connect()
   # user_id = int(session.get("user_id"))
    for row in con.run("SELECT * FROM Article_Ref"):
        print(row, "ok")
    con.close()