from django.test import TestCase
from core.constrains import NAME, ABOUT, IMAGE
from authors.models import Author

class TestModelAuthor(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author_data = {
            NAME: "Fiódor Dostoiévski",
            ABOUT: "Foi escritor, filósofo e jornalista do Império Russo"
        }
        cls.author_instance = Author.objects.create(**cls.author_data)

    def test_author_fields(self):
        fields = [NAME, ABOUT]
        for field in fields:
            result = getattr(self.author_instance, field)
            expected = self.author_data[field]
            msg = f'Checking if {field} is the same'
            self.assertEqual(result, expected, msg)
