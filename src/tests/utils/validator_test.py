import unittest
from src.utils.validator import Validator

class TestValidator(unittest.TestCase):
    
    def test_required_fields_not_filled(self):
        data = dict(
                reference_id="uniq1",
                reference_name="ARTICLE",
                author="author",
                journal="",
                title="title",
                year="15"
            )
        validator = Validator(data)
        validator.run_all_validators()
        self.assertEqual(validator.error, "Vaadittu kenttä täyttämättä: journal")
    
    def test_required_id_not_filled(self):
        data = dict(
                reference_id="",
                reference_name="ARTICLE",
                author="author",
                journal="journal",
                title="title",
                year="15"
            )
        validator = Validator(data)
        validator.run_all_validators()
        self.assertEqual(validator.error, "Vaadittu kenttä täyttämättä: reference_id")
    
    def test_both_of_or_forms_filled(self):
        data = dict(
                reference_id="123",
                reference_name="BOOK",
                author="author",
                editor="editor",
                title="title",
                publisher="publisher",
                year="15"
            )

        validator = Validator(data)
        validator.run_all_validators()
        self.assertEqual(validator.error, "Vain toinen kentistä author ja editor voi sisältää tietoa")
    
    def test_too_long_form(self):
        data = dict(
                reference_id="123",
                reference_name="BOOK",
                author="author",
                title="title",
                publisher="publisheraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                year="15"
            )

        validator = Validator(data)
        validator.run_all_validators()
        self.assertEqual(validator.error, "publisher ei voi olla pidempi kuin 120 kirjainta")
