import unittest
from app import app
from src.services.user import *
from src.utils.db import connect

class TestUserRoute(unittest.TestCase):
    def setUp(self):
        query = "DELETE FROM Users"
        con = connect()
        con.run(query)
        con.close()
        register("testaaja", "testaaja")
        self.client = app.test_client()
    
    def test_register_post_valid(self):
        resp = self.client.post("/register", data=dict(
          username="thisisvalid", 
          password1="topsekret", 
          password2="topsekret"
          ))
        
        self.assertEqual(resp.status_code, 201)

    def test_register_post_invalid_username(self):
        resp = self.client.post("/register", data=dict(
          username="th", 
          password1="topsekret", 
          password2="topsekret"
          ))
        
        self.assertEqual(resp.status_code, 400)

    def test_register_post_different_passwords(self):
        resp = self.client.post("/register", data=dict(
            username="valid",
            password1="topsekret",
            password2="topsecret"
        ))

        self.assertEqual(resp.status_code, 400)

    def test_login_incorrect_credentials(self):
        resp = self.client.post("/login", data=dict(
            username="eiolemassa",
            password="topsekret"
        ))

        self.assertEqual(resp.status_code, 400)

# Nämä kaksi alempaa ei toimi
    def test_login_correct_credentials(self):
        resp = self.client.post("/login", data=dict(
            username="testaaja",
            password="testaaja"
        ))

        self.assertEqual(resp.status_code, 200)

    def test_logout_when_logged_in(self):
        resp = self.client.get("/logout")
        self.assertEqual(resp.status_code, 200)
