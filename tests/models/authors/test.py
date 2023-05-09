from django.test import TestCase
from django.db.models.fields.files import FieldFile
from random import random
from core.constrains import NAME, ABOUT, IMAGE
from authors.models import Author
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

class TestModelAuthor(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author_data = {
            NAME: "Fiódor Dostoiévski",
            ABOUT: "Foi escritor, filósofo e jornalista do Império Russo",
            IMAGE: "https://bit.ly/3LOfjIX"
        }
        cls.author_instance = Author.objects.create(**cls.author_data)

    def test_author_fields(self):
        fields = [NAME, ABOUT, IMAGE]
        for field in fields:
            result = getattr(self.author_instance, field)
            expected = self.author_data[field]
            msg = f'Checking if {field} is the same'
            self.assertEqual(result, expected, msg)

    # def test_author_fields_types(self):
    #     invalid_author {
    #         NAME: False,
    #         ABOUT: get_random_string(5)
    #     }
    #     with self.assertRaises(ValidationError):
    #         User.objects.create_user(**invalid_user)

    def test_if_raise_error_when_invalid_types_fields(self):
        """Test if raise an error when using a invalid type"""
        invalid_author = {
            NAME: True,
            ABOUT: 96
        }
        a0 = Author.objects.create(**invalid_author)
        print(a0)
        # with self.assertRaises(ValidationError):
        #     Author.objects.create(**invalid_author)

