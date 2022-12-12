import unittest
import os
from app import app
from src.utils.db import connect
from src.services.reference import *

class TestReferenceRoute(unittest.TestCase):
    def setUp(self):
        self.con = connect()
        self.cur = self.con.cursor()
        self.cur.execute("DELETE FROM tblReference")
        self.cur.execute("DELETE FROM Users")
        self.cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING id", ("user", "12345678"))
        result = self.cur.fetchone()
        self.con.commit()

        self.user_id = result[0]
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user_id

    
    def test_invalid_type_name_fetch(self):
        resp = self.client.get("/add/thisisinvalid")
        self.assertEqual(resp.status_code, 404)
    
    def test_add_valid_reference_name_fetch(self):
        resp = self.client.get("/add/ARTICLE", follow_redirects=True)
        self.assertIn("<h1>Lisää viite: Artikkeli", resp.text)
    
    def test_add_invalid_reference_name(self):
        resp = self.client.post("/add", data=dict(
                reference_name="thisisinvalid"
            ))
        self.assertEqual(resp.status_code, 404)
    
    def test_add_required_fields_not_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="uniq1",
                reference_name="ARTICLE",
                author="author",
                journal="",
                title="title",
                year="15"
            ), follow_redirects=True)
        self.assertIn("Vaadittu kenttä täyttämättä:", resp.text)
    
    def test_add_required_id_not_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="",
                reference_name="ARTICLE",
                author="author",
                journal="journal",
                title="title",
                year="15"
            ), follow_redirects=True)
        self.assertIn("Vaadittu kenttä täyttämättä:", resp.text)
    
    def test_add_both_of_or_forms_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="123",
                reference_name="BOOK",
                author="author",
                editor="editor",
                title="title",
                publisher="publisher",
                year="15"
            ), follow_redirects=True)
        self.assertIn("Vain toinen kentistä author ja editor voi sisältää tietoa", resp.text)

    def test_add_other_of_or_forms_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisher",
                year="15",
            ), follow_redirects=True)
        self.assertIn("Lisätyt viitteet", resp.text)
    
    def test_validation_error_in_form(self):
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisher",
                year="123abc",
            ), follow_redirects=True)
        self.assertIn("arvon tulee olla kokonaisluku</h2>", resp.text)

    def test_validation_error_in_form_optional(self):
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisher",
                year="123",
                volume="123",
                number="123",
            ), follow_redirects=True)
        self.assertIn("Vain toinen kentistä volume ja number voi sisältää tietoa", resp.text)

    def test_add_duplicate_id(self):
        self.client.post("/add", data=dict(
                reference_id="niceid",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisher",
                year="123",
                volume="123",
            ))
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisher",
                year="123",
            ), follow_redirects=True)
        self.assertIn("on jo käytössä", resp.text)
    
    def test_addbib_template(self):
        resp = self.client.get("/addbib")
        self.assertEqual(resp.status_code, 200)

    def test_finddoi_empty_doi(self):
        resp = self.client.post("/finddoi", data=dict(
                doi="",
            ), follow_redirects=True)
        self.assertIn("Et täyttänyt DOI kenttää", resp.text)

    def test_finddoi_valid_doi(self):
        resp = self.client.post("/finddoi", data=dict(
                doi="10.1145/2380552.2380613",
            ), follow_redirects=True)
        self.assertIn("@article{2012", resp.text)

    def test_add_by_doi_valid(self):
        bib = """@article{CitekeyArticle, author=\"P. J. Cohen\",
            title=\"The independence of the continuum hypothesis\",
            journal=\"Proceedings of the National Academy of Sciences\",
            year=1963,
            volume=\"50\",
            number=\"6\",
            pages=\"1143--1148\",
            }
        """

        resp = self.client.post("/addbibdb", data=dict(
                addbib=bib,
            ), follow_redirects=True)
        self.assertIn("Lisätyt viitteet", resp.text)

    def test_add_by_doi_invalid(self):
        bib = """@article{CitekeyArticle, author=\"P. J. Cohen\",
            title=\"The independence of the continuum hypothesis\",
            journal=\"Proceedings of the National Academy of Sciences\",
            year="aaa",
            volume=\"50\",
            number=\"6\",
            pages=\"1143--1148\",
            }
        """

        resp = self.client.post("/addbibdb", data=dict(
                addbib=bib,
            ), follow_redirects=True)
        self.assertIn("kokonaisluku", resp.text)

    def test_add_by_doi_duplicate(self):
        bib = """@article{CitekeyArticle, author=\"P. J. Cohen\",
            title=\"The independence of the continuum hypothesis\",
            journal=\"Proceedings of the National Academy of Sciences\",
            year=1963,
            volume=\"50\",
            number=\"6\",
            pages=\"1143--1148\",
            }
        """

        resp = self.client.post("/addbibdb", data=dict(
                addbib=bib,
            ), follow_redirects=True)
        
        resp = self.client.post("/addbibdb", data=dict(
                addbib=bib,
            ), follow_redirects=True)

        self.assertIn("on jo käytössä!", resp.text)

    def test_validation_search_form(self):
        resp = self.client.post("/search", data=dict(
                search_author="author",
                search_year="15",
            ), follow_redirects=True)
        self.assertIn("user", resp.text)

    def test_validation_error_search_form(self):
        resp = self.client.post("/search", data=dict(
                search_author="",
                search_year="",
            ), follow_redirects=True)
        self.assertIn("Hakusi ei tuottanut tulosta. Ole hyvä ja yritä uudelleen.",
        resp.text)

        resp = self.client.post("/search", data=dict(
                search_author="",
                search_year="2022-",
            ), follow_redirects=True)
        self.assertIn( "Annoit vuoden väärässä muodossa. Ole hyvä ja yritä uudelleen.",
        resp.text)

        resp = self.client.post("/search", data=dict(
                search_author="",
                search_year="aAA",
            ), follow_redirects=True)
        self.assertIn("Vuosi tulee antaa kokonaislukuna. Ole hyvä ja yritä uudelleen.",
        resp.text)
