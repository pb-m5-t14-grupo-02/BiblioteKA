from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    book_loan = models.ManyToManyField(
        "books.Copy",
        through="books.BookLoan",
        related_name="copies"
    )