from django.test import TestCase
from books.models import Book, Copy
from authors.models import Author
from django.core.exceptions import ValidationError
from core.constrains import USER, COPY, IS_AVALIABLE
from tests.models.common import create_author_data, create_book_data
from random import random


class TestModelBookLoan(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(**create_author_data())
        cls.book = Book.objects.create(**create_book_data(author=author))
        cls.copies = [Copy.objects.create(book=cls.book) for _ in range(0, 10)]

    def setUp(self) -> None:
        self.copy = Copy.objects.create(book=self.book)

    def test_verify_types_fields(self):
        """Test if types of fields are correctly"""
        result = type(self.copy.is_avaliable)
        expected = bool
        self.assertEqual(result, expected)

    def test_if_raise_error_when_invalid_types_fields(self):
        """Test if raise an error when using a invalid type"""
        invalid_copy = {IS_AVALIABLE: random()}
        with self.assertRaises(ValidationError):
            Copy.objects.create(**invalid_copy)

    def test_copy_field_is_avaliable_content(self):
        """Testing if field is_avaliable is correct added to database"""
        result = self.copy.is_avaliable
        expected = True
        self.assertEqual(result, expected)

    def test_ensure_default_field(self):
        """Testing if field is_avaliable has the correct default value"""
        result = self.copy._meta.get_field(IS_AVALIABLE).default
        expected = True
        self.assertEqual(result, expected)
