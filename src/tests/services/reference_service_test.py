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
        self.cur.execute("ALTER SEQUENCE tblReference_id_seq RESTART WITH 1")
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

        bibtex_string = generate_bibtex_string(ref)
        self.assertIn("@article{uniq1", bibtex_string)
        self.assertIn("author = {", bibtex_string)
        self.assertIn("journal = {", bibtex_string)
    
    def test_bibtex_in_bytes(self):
        some_str = "asdasdasd"
        self.assertEqual(get_bibtex_in_bytes(some_str).getvalue(), b"asdasdasd")
    
    def test_from_bibtexparser_to_db(self):
        entries = [{
            "ENTRYTYPE": "book",
            "ID": "asd"
        }]
        from_bibtexparser_to_db(entries)

        self.assertEqual(entries[0].get("ENTRYTYPE"), None)
        self.assertEqual(entries[0].get("ID"), None)
        self.assertEqual(entries[0].get("reference_name"), "BOOK")
        self.assertEqual(entries[0].get("reference_id"), "asd")
        
    def test_find_by_doi_valid(self):
        result = find_bib_by_doi("10.1145/2380552.2380613")
        self.assertIn("@article{2012", result)
        
    def test_find_by_doi_invalid(self):
        result = find_bib_by_doi("10.1145/2380552.2380613aaaaa")
        self.assertIn("ei löytynyt", result)

    def test_reference_deletion_works_only_with_correct_credentials(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq2", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq3", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq4", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        self.assertEqual(len(get_references(self.user_id)), 4)
        id1 = get_references(self.user_id)[0]["id"]
        id2 = get_references(self.user_id)[1]["id"]
        id3 = get_references(self.user_id)[2]["id"]
        id4 = get_references(self.user_id)[3]["id"]
        delete_selected([self.user_id, id1])
        self.assertEqual(len(get_references(self.user_id)), 3)
        delete_selected([self.user_id, id2, id3])
        self.assertEqual(len(get_references(self.user_id)), 1)
        delete_selected([int(self.user_id)+1, id4])
        self.assertEqual(len(get_references(self.user_id)), 1)
        
    def test_filter_selected_from_references(self):
        add_reference(self.user_id, "uniq1", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq2", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq3", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        add_reference(self.user_id, "uniq4", "ARTICLE", ["author", "journal"], ["jotai1", "jotai2"])
        selected_id = ['1','3']
        entries = get_references(self.user_id)
        filtered = get_selected(entries, selected_id)
        self.assertEqual(filtered[0]["id"], 1)
        self.assertEqual(filtered[1]["id"], 3)
        
