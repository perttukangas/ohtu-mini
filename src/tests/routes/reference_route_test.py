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
    
    def test_add_valid_type_name_fetch(self):
        resp = self.client.get("/add/ARTICLE", follow_redirects=True)
        self.assertIn("<h1>Lisää viite: Artikkeli", resp.text)
    
    def test_add_invalid_type_name(self):
        resp = self.client.post("/add", data=dict(
                type_name="thisisinvalid"
            ))
        self.assertEqual(resp.status_code, 404)
    
    def test_add_required_fields_not_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="uniq1",
                type_name="ARTICLE",
                author="author",
                journal="",
                title="title",
                year="15"
            ), follow_redirects=True)
        self.assertIn("Vaadittu kenttä täyttämättä:", resp.text)
    
    def test_add_required_id_not_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="",
                type_name="ARTICLE",
                author="author",
                journal="journal",
                title="title",
                year="15"
            ), follow_redirects=True)
        self.assertIn("Vaadittu kenttä täyttämättä:", resp.text)
    
    def test_add_both_of_or_forms_filled(self):
        resp = self.client.post("/add", data=dict(
                reference_id="123",
                type_name="BOOK",
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
                type_name="BOOK",
                author="author",
                editor="",
                title="title",
                publisher="publisher",
                year="15",
                volume="",
                number="",
                series="",
                address="",
                edition="",
                month="",
                note=""
            ), follow_redirects=True)
        self.assertIn("Tervetuloa etusivulle", resp.text)
    
    def test_validation_error_in_form(self):
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                type_name="BOOK",
                author="author",
                editor="",
                title="title",
                publisher="publisher",
                year="123abc",
                volume="",
                number="",
                series="",
                address="",
                edition="",
                month="",
                note=""
            ), follow_redirects=True)
        self.assertIn("arvon tulee olla kokonaisluku</h2>", resp.text)

    def test_validation_error_in_form_optional(self):
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                type_name="BOOK",
                author="author",
                editor="",
                title="title",
                publisher="publisher",
                year="123",
                volume="123",
                number="123",
                series="",
                address="",
                edition="",
                month="",
                note=""
            ), follow_redirects=True)
        self.assertIn("Vain toinen kentistä volume ja number voi sisältää tietoa", resp.text)

    def test_add_duplicate_id(self):
        self.client.post("/add", data=dict(
                reference_id="niceid",
                type_name="BOOK",
                author="author",
                editor="",
                title="title",
                publisher="publisher",
                year="123",
                volume="123",
                number="",
                series="",
                address="",
                edition="",
                month="",
                note=""
            ))
        resp = self.client.post("/add", data=dict(
                reference_id="niceid",
                type_name="BOOK",
                author="author",
                editor="",
                title="title",
                publisher="publisher",
                year="123",
                volume="",
                number="",
                series="",
                address="",
                edition="",
                month="",
                note=""
            ), follow_redirects=True)
        self.assertIn("on jo käytössä", resp.text)

    def test_file_download(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        resp = self.client.get("/download-file", follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
