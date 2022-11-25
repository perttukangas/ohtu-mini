import unittest
from src.services.user import *
from src.utils.db import connect

class TestUserService(unittest.TestCase):
    def setUp(self):
        query = "DELETE FROM Users"
        self.con = connect()
        self.con.run(query)
    
    def test_valid_register(self):
        username = "testuser"
        self.assertEqual(register(username, "topsekret"), True)
        
        query = "SELECT username FROM Users WHERE username=:username"
        user = self.con.run(query, username=username)[0]
        self.assertEqual(user[0], username)

        self.con.close()
        
    def test_password_is_hashed(self):
        pass
