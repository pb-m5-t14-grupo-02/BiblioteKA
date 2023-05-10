from django.test import TestCase
from django.db.models.fields.files import FieldFile
from core.constrains import NAME, ABOUT, IMAGE
from authors.models import Author
from tests.models.common import create_author_data


class TestModelAuthor(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author_data = create_author_data(
            "Fiódor Dostoiévski",
            "Foi escritor, filósofo e jornalista do Império Russo",
            "https://bit.ly/3LOfjIX"
        )
        cls.author_instance = Author.objects.create(**cls.author_data)

    def test_author_fields_content(self):
        """Testing if all model fields are correctly added to database"""
        fields = (NAME, ABOUT, IMAGE)
        for field in fields:
            result = getattr(self.author_instance, field)
            expected = self.author_data[field]
            msg = f"Checking if {field} is the same"
            self.assertEqual(result, expected, msg)

    def test_fields_max_length(self):
        """Test if the max length of this field is right"""
        result = self.author_instance._meta.get_field(ABOUT).max_length
        expected = None
        self.assertEqual(result, expected)

        result = self.author_instance._meta.get_field(NAME).max_length
        expected = 120
        self.assertEqual(result, expected)

    def test_verify_types_fields(self):
        """Test if types of fields are correctly"""
        string_fields = (NAME, ABOUT)
        expected = str
        for field in string_fields:
            result = type(getattr(self.author_instance, field))
            self.assertEqual(result, expected)

        result = type(self.author_instance.image)
        expected = FieldFile
        self.assertEqual(result, expected)
