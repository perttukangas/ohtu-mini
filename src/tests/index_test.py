import unittest
from app import app

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/ping')
        self.assertEqual(response.text, "pong")

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_test_page(self):
        response = self.client.get("/test")
        self.assertEqual(response.status_code, 200)
