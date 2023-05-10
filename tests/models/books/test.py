from django.test import TestCase
from authors.models import Author
from django.db.models.fields.files import FieldFile
from django.utils.crypto import get_random_string as grs
from books.models import Book
from core.constrains import NAME, SERIES, GENRE, ABOUT, YEAR, DAYS, ISBN, ASIN, IMAGE
from tests.models.common import create_author_data, create_book_data


class TestModelBook(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author_1 = Author.objects.create(**create_author_data())
        cls.book_data = create_book_data(
            name="A sociedade do Anel",
            about="Foi o primeiro grande épico de fantasia moderno",
            series="Senhor dos Anéis",
            genre="adventure",
            year=1954,
            days=14,
            isbn="9786501252277",
            asin="B08Z5NYG12",
            image="https://bit.ly/3pqebnw",
            author=cls.author_1
        )
        cls.book_instance = Book.objects.create(**cls.book_data)

    def test_books_fields(self):
        """Testing if all model fields are correctly added to database"""
        fields = (NAME, SERIES, GENRE, ABOUT, YEAR, DAYS, ISBN, ASIN, IMAGE)
        for field in fields:
            result = getattr(self.book_instance, field)
            expected = self.book_data[field]
            msg = f'Checking if {field} is the same'
            self.assertEqual(result, expected, msg)

    def test_verify_types_fields(self):
        """Test if types of fields are correctly"""
        string_fields = (NAME, SERIES, GENRE, ABOUT, ISBN, ASIN)
        expected = str
        for field in string_fields:
            result = type(getattr(self.book_instance, field))
            self.assertEqual(result, expected)

        result = type(self.book_instance.year)
        expected = int
        self.assertEqual(result, expected)

        result = type(self.book_instance.image)
        expected = FieldFile
        self.assertEqual(result, expected)

    def test_if_fields_can_be_null(self):
        """Test if these fields can be nullable"""
        nullable_fields = (SERIES, GENRE, ISBN, ASIN)
        for field in nullable_fields:
            nullable = self.book_instance._meta.get_field(field).null
            self.assertTrue(nullable)

    def test_fields_max_length(self):
        """Test if the max length of this field is right"""
        result = self.book_instance._meta.get_field(NAME).max_length
        expected = 120
        self.assertEqual(result, expected)

        result = self.book_instance._meta.get_field(GENRE).max_length
        self.assertEqual(result, expected)

        result = self.book_instance._meta.get_field(ABOUT).max_length
        expected = None
        self.assertEqual(result, expected)

        result = self.book_instance._meta.get_field(ISBN).max_length
        expected = 13
        self.assertEqual(result, expected)

        result = self.book_instance._meta.get_field(ASIN).max_length
        expected = 10
        self.assertEqual(result, expected)

    def test_if_raise_error_when_invalid_types_fields(self):
        """Test if raise an error when using a invalid type"""
        invalid_book = create_book_data(year=grs(5))
        with self.assertRaises(ValueError):
            Book.objects.create(**invalid_book)

    def test_if_raise_eror_when_invalid_types_fields(self):
        invalid_book = create_book_data(days=17)
        with self.assertRaises(ValueError):
            Book.objects.create(**invalid_book)
