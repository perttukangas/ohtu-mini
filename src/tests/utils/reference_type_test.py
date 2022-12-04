import unittest
from src.utils import reference_type

class TestReferenceTypeTest(unittest.TestCase):
    def setUp(self):
        self.ref_type = reference_type.ReferenceType.BOOK
    
    def test_correct_constants(self):
        self.assertEqual(self.ref_type.get_name(), "Kirja (@book)")
        self.assertEqual(self.ref_type.get_required(), 
        [("author", "editor"), "title", "publisher", "year"])
        self.assertEqual(self.ref_type.get_optional(), 
        [("volume", "number"), "series", "address", "edition", "month", "note"])
    
    def test_required_for_add(self):
        req = self.ref_type.get_required_for_add()

        self.assertEqual(req[0][0][0], "author")
        self.assertEqual(req[0][1][0], "editor")

        self.assertEqual(req[1][0], "title")
        self.assertEqual(req[2][0], "publisher")
        self.assertEqual(req[3][0], "year")

    def test_optional_for_add(self):
        req = self.ref_type.get_optional_for_add()

        self.assertEqual(req[0][0][0], "volume")
        self.assertEqual(req[0][1][0], "number")

        self.assertEqual(req[1][0], "series")
        self.assertEqual(req[2][0], "address")
        self.assertEqual(req[3][0], "edition")
        self.assertEqual(req[4][0], "month")
        self.assertEqual(req[5][0], "note")
    
    def test_get_references_for_index(self):
        result = reference_type.get_references_for_index()
        self.assertEqual(result[0], ("ARTICLE", "Artikkeli (@article)"))
        self.assertEqual(result[1], ("BOOK", "Kirja (@book)"))
    
    def test_get_references_cache_for_index(self):
        reference_type.get_references_for_index()
        result = reference_type.cache_references_for_index
        self.assertEqual(result[0], ("ARTICLE", "Artikkeli (@article)"))
        self.assertEqual(result[1], ("BOOK", "Kirja (@book)"))
