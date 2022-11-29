from flask import session
from src.utils.db import connect

def add_reference(ref_id, user_id, author, heading, magazine, year, volume, doi,
publisher, pages):
    """Funktio lisää artikkeliviitteen tiedot tietokantaan.
    """

    query = '''INSERT INTO Article_Ref (ref_id, user_id, author, heading,
    magazine, year, volume, doi, publisher, pages) VALUES (:ref_id, :user_id,
    :author, :heading, :year, :magazine, :volume, :doi, :publisher, :pages)'''
    con = connect()

    try:
        con.run(query, ref_id=ref_id, user_id=user_id, author=author,
        heading=heading, magazine=magazine, year=year, volume=volume, doi=doi,
        publisher=publisher, pages=pages)
        con.close()
    except:
        con.close()
        return False
    return True

def check_validation(ref_id, author, heading, magazine, year):
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
    if len(magazine) < 2 or len(magazine) > 200:
        error_msg = "Lehden nimi on liian lyhyt tai liian pitkä"
    if len(year) != 4:
        error_msg = "Vuosiluku annettu väärin"

    user_id = int(session.get("user_id"))
    query2 = '''SELECT ref_id FROM Article_Ref WHERE user_id=:user_id AND
    ref_id=:ref_id'''
    con = connect()
    unique_id = con.run(query2, ref_id=ref_id, user_id=user_id)
    con.close()
    if unique_id != []:
        error_msg = "ID-tunnus on jo käytössä. Kokeile toista."

    return error_msg

def get_references():
    """Funktio hakee listan viitteistä kirjautuneen käyttäjän id:n perusteella.
    Palautetaan lista, johon laitettu mukaan muotoilu.
    """

    user_id = int(session.get("user_id"))
    query = '''SELECT author, heading, magazine, year, volume, doi, publisher,
    pages FROM Article_Ref WHERE user_id=:user_id'''

    con = connect()

    try:
        ref_list = con.run(query, user_id=user_id)
        lista = []
        for list in ref_list:
            web_modified_list = []
            if list[0]: #author
                list[0] += ". "
                web_modified_list.append(list[0])
            if list[1]: #heading
                list[1] += ". "
                web_modified_list.append(list[1])
            if list[3]: #year
                list[3] += ". "
                web_modified_list.insert(len(web_modified_list), list[3])
            if list[2] and list[4] == '' and list[7] == '': #magazine, volume, pages
                list[2] += ". "
                web_modified_list.append(list[2])
            if list[2] and list[4] != '' and list[7] != '': #magazine, volume, pages
                list[2] += ". "
                list[2] += (list[4] + ":")
                list[2] += (list[7] + ", ")
                web_modified_list.append(list[2])
            if list[2] and list[4] == '' and list[7] != '': #magazine, volume, pages
                list[2] += ", "
                list[2] += list[7] + ". "
                web_modified_list.append(list[2])
            if list[2] and list[4] != '' and list[7] == '': #magazine ja volume löytyy
                list[2] += ", "
                list[2] += list[4] + ". "
                web_modified_list.append(list[2])
            if list[6] != '': #publisher
                list[6] += ". "
                web_modified_list.append(list[6])
            if list[5] != '': #doi
                list[5] += "."
                web_modified_list.insert(len(web_modified_list), list[5])
            lista.append(web_modified_list)
        con.close()
        return lista
    except:
        con.close()
        return []
