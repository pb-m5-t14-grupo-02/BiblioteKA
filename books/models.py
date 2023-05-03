from django.db import models
from core.constrains import way, USERS, USER, COPY, AUTHOR, AUTHORS, BOOK, BOOKS

class Book(models.Model):
    image = models.TextField(default="https://i.postimg.cc/J7H4ryhJ/51s-Is-L2-Hpp-L-SX337-BO1-204-203-200-cleanup.png")
    name = models.CharField(max_length=120)
    series = models.CharField(max_length=120, null=True, default=None)
    genre = models.CharField(max_length=120, null=True, default=None)
    about = models.TextField()
    year = models.IntegerField()
    copies_count = models.IntegerField()
    ISBN = models.CharField(max_length=13, null=True, default=None)
    ASIN = models.CharField(max_length=10, null=True, default=None)
    following = models.ManyToManyField(
        way(USERS, USER),
        related_name="followed_books"
    )
    author = models.ForeignKey(
        way(AUTHORS, AUTHOR),
        on_delete=models.CASCADE,
        related_name="books"
    )

class BookLoan(models.Model):
    user = models.ForeignKey(
        way(USERS, USER),
        on_delete=models.CASCADE,
    )
    copy = models.ForeignKey(
        way(BOOKS, COPY),
        on_delete=models.CASCADE,
    )
    load_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class Copy(models.Model):
    book = models.ForeignKey(
        way(BOOKS, BOOK),
        on_delete=models.CASCADE,
        related_name="copies"
    )