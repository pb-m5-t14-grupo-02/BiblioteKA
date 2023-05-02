from django.db import models
from django.contrib.auth.models import AbstractUser
from core.constrains import way, BOOKS, COPY, BOOK_LOAN

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    book_loan = models.ManyToManyField(
        way(BOOKS, COPY),
        through=way(BOOKS, BOOK_LOAN),
        related_name="copies"
    )
