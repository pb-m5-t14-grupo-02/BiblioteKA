from django.test import TestCase
from authors.models import Author
from books.models import Book
from core.constrains import NAME, SERIES, GENRE, ABOUT, YEAR, DAYS, ISBN, ASIN, IMAGE

# name = models.CharField(max_length=120)
#     series = models.CharField(max_length=120, null=True, default=None)
#     genre = models.CharField(max_length=120, null=True, default=None)
#     about = models.TextField()
#     year = models.IntegerField()
#     days = models.IntegerField(default=LoanDays.week, choices=LoanDays.choices)
#     ISBN = models.CharField(max_length=13, null=True, default=None)
#     ASIN = models.CharField(max_length=10, null=True, default=None)
class TestModelBook(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book_data = {
            NAME: "A sociedade do Anel",
            ABOUT: "Foi o primeiro grande épico de fantasia moderno",
            SERIES: "Senhor dos Anéis",
            GENRE: "adventure",
            YEAR: 1954,
            DAYS: 14,
            ISBN: "978–65–012–5227–7",
            ASIN: "B08Z5NYG12",
            IMAGE: "https://bit.ly/3pqebnw"
        }


