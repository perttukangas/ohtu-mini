import unittest
from src.utils.validator import Validator, check_for_errors

class TestValidatorTest(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()

    def test_validator_object_created_successfully(self):
        self.assertEqual(self.validator.has_errors(), False)

    def test_year_input_check_works_correctly(self):
        self.validator.year_input_correctly("author", "Mika Waltari")
        self.assertEqual(self.validator.has_errors(), False)
        self.validator.year_input_correctly("year", "2022")
        self.assertEqual(self.validator.has_errors(), False)
        self.validator.year_input_correctly("year", "banaani")
        self.assertEqual(self.validator.has_errors(), True)

    def test_length_check_works_as_intended(self):
        self.assertEqual(self.validator.has_errors(), False)
        self.validator.has_length_less_than("author", "Aku Ankka")
        self.assertEqual(self.validator.has_errors(), False)
        self.validator.has_length_less_than("address", "abc"*250)
        self.assertEqual(self.validator.has_errors(), True)
