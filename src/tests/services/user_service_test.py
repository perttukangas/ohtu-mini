import unittest
from src.services.user import *
from src.utils.db import connect
from werkzeug.security import check_password_hash, generate_password_hash

class TestUserService(unittest.TestCase):
    def setUp(self):
        query = "DELETE FROM Users"
        self.password = "topsekret"
        self.con = connect()
        self.con.run(query)
        register("testaaja","testaaja")


    def test_valid_register(self):
        username = "testuser1"
        self.assertEqual(register(username, self.password), True)
        
        query = "SELECT username FROM Users WHERE username=:username"
        user = self.con.run(query, username=username)[0]
        self.assertEqual(user[0], username)
        self.con.close()

    def test_user_exists(self):
        self.assertNotEqual(check_user_exists("testaaja"), False)
        self.assertEqual(check_user_exists("tttttttt"), False)

# Tämä testataan jo user_route_test.py, ei ehkä tarpeellinen
#    def test_valid_login(self):
#        self.assertEqual(login("testaaja", "testaaja"), True)


    def test_login_wrong_password(self):
        username = "testuser"
        self.assertEqual(login(username, self.password+"aa"), False)
