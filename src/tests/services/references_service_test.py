import unittest
from app import app
from src.services.references import *
from src.utils.db import connect

class TestReferencesService(unittest.TestCase):
    def setUp(self):
        query = 'DELETE FROM Article_Ref'
        query2 = 'DELETE FROM Users'
        query3 = 'ALTER SEQUENCE Users_id_seq RESTART WITH 1'
        self.con = connect()
        self.con.run(query)
        self.con.run(query2)
        self.con.run(query3)
        self.user_id = 1

    def test_reference_is_added(self):
        query1 = "INSERT INTO Users (username, password) VALUES ('testeri', 'testisalis')"
        self.con.run(query1)
        query2 = "SELECT id FROM Users WHERE username=:username"
        user_id = self.con.run(query2, username='testeri')[0]
        print(user_id)
        
        ref_id = '1234'
        author = 'Maija Meikalainen'
        heading = 'Testi'
        magazine = 'Testaajat'
        year = '2022'
        volume = ''
        doi = ''
        publisher = ''
        pages = ''
        
        self.assertEqual(add_reference(ref_id, self.user_id, author, heading, magazine, year, volume, doi, publisher, pages), True)
        self.con.close()
        
    def test_reference_is_shown_in_list(self):
        query2 = "SELECT id FROM Users WHERE username=:username"
        user_id = self.con.run(query2, username='testeri')[0]
        print(user_id)
        query1 = '''INSERT INTO Article_Ref (ref_id, user_id, author, heading,
            magazine, year, volume, doi, publisher, pages) VALUES ('99', 1,
            'Testinen', 'Testaus', 2000, '', '', '', '', '')'''
        self.con.run(query1)
        test_list = get_references()
        print(test_list)
        self.con.close()
        