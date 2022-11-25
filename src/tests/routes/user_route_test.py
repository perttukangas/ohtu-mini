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
