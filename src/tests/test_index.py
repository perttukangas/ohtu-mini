import unittest
from app import app

class TestIndex(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get('/ping')
        self.assertEqual(response.text, "pong")
