import unittest
from src.services.user import *
from src.utils.db import connect

class TestUserService(unittest.TestCase):
    def setUp(self):
        query = "DELETE FROM Users"
        self.password = "topsekret"
        self.con = connect()
        self.cur = self.con.cursor()
        self.cur.execute(query)
        self.con.commit()
        register("testaaja","testaaja")


    def test_valid_register(self):
        username = "testuser1"
        self.assertEqual(register(username, self.password), True)
        query = "SELECT username FROM Users WHERE username=%s"
        self.cur.execute(query, (username,))
        self.assertEqual(self.cur.fetchone()[0], username)
        self.con.close()

    def test_user_exists(self):
        self.assertNotEqual(check_user_exists("testaaja"), False)
        self.assertEqual(check_user_exists("tttttttt"), False)

    def test_login_wrong_password(self):
        username = "testuser"
        self.assertEqual(login(username, self.password+"aa"), False)
