from pg8000.exceptions import DatabaseError
import unittest
from src.services.reference import *
from src.utils.db import connect
from os.path import exists
import os

class TestReferenceService(unittest.TestCase):
    def setUp(self):
        self.con = connect()
        self.cur = self.con.cursor()
        self.cur.execute("DELETE FROM tblReference")
        self.cur.execute("DELETE FROM Users")
        self.cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING id", ("user", "12345678"))
        result = self.cur.fetchone()
        
        self.con.commit()
        self.user_id = result[0]

    def test_add_reference_valid(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        refs = get_references(self.user_id)

        self.assertEqual(refs[0]["user_id"], self.user_id)
        self.assertEqual(refs[0]["reference_id"], "uniq1")
        self.assertEqual(refs[0]["reference_name"], "ARTICLE")
        self.assertEqual(refs[0]["author"], "jotai1")
        self.assertEqual(refs[0]["journal"], "jotai2")
    
    def test_add_reference_duplicate_ref_id(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        with self.assertRaises(DatabaseError):
            add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["asd1", "asd2"])
    
    def test_add_reference_duplicate_ref_id_other_user(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])

        self.cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s) RETURNING id", ("user2", "12345678"))
        result = self.cur.fetchone()
        self.con.commit()

        add_reference(result[0], "uniq1", "ARTICLE", ["author", "journal"], ["asd1", "asd2"])
        # Tää testi onnistuu, kun ylempi rivi ei raisee exceptionii
    
    def test_get_references(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq2", "ARTICLE", ["author", "journal"], ["jotai3", "jotai4"])
        refs = get_references(self.user_id)

        self.assertEqual(len(refs), 2)

        self.assertEqual(refs[0]["user_id"], self.user_id)
        self.assertEqual(refs[0]["reference_id"], "uniq1")
        self.assertEqual(refs[0]["reference_name"], "ARTICLE")
        self.assertEqual(refs[0]["author"], "jotai1")
        self.assertEqual(refs[0]["journal"], "jotai2")

        self.assertEqual(refs[1]["user_id"], self.user_id)
        self.assertEqual(refs[1]["reference_id"], "uniq2")
        self.assertEqual(refs[1]["reference_name"], "ARTICLE")
        self.assertEqual(refs[1]["author"], "jotai3")
        self.assertEqual(refs[1]["journal"], "jotai4")

    def test_generate_bibtex_string(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        ref = get_references(self.user_id)

        generate_bibtex_string(ref, self.user_id)
        self.assertTrue(exists(f'src/services/bibtex_files/bibtex_{self.user_id}.bib'))

        os.remove(f'src/services/bibtex_files/bibtex_{self.user_id}.bib')