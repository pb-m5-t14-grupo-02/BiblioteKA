from django.db import models
from core.constrains import (
    USERS,
    USER,
    COPY,
    AUTHOR,
    AUTHORS,
    BOOK,
    BOOKS,
    BOOK_LOAN,
    way,
    repr_default,
)
import datetime


class LoanDays(models.IntegerChoices):
    week = 7
    fortnight = 15
    month = 30


class BookFollowing(models.Model):
    user = models.ForeignKey(
        way(USERS, USER),
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        way(BOOKS, BOOK),
        on_delete=models.CASCADE,
    )
    

class Book(models.Model):
    image = models.FileField(
        upload_to="books",
        max_length=1000,
        default="https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683571699/defaults/book/book_kzgg3h.png",
    )
    name = models.CharField(max_length=120)
    series = models.CharField(max_length=120, null=True, default=None)
    genre = models.CharField(max_length=120, null=True, default=None)
    about = models.TextField()
    year = models.IntegerField()
    days = models.IntegerField(default=LoanDays.week, choices=LoanDays.choices)
    ISBN = models.CharField(max_length=13, null=True, default=None)
    ASIN = models.CharField(max_length=10, null=True, default=None)
    following = models.ManyToManyField(way(USERS, USER), related_name="followed_books", through=BookFollowing)
    author = models.ForeignKey(
        way(AUTHORS, AUTHOR), on_delete=models.CASCADE, related_name="books"
    )

    def __repr__(self) -> str:
        return repr_default(BOOK, self.pk, self.name)


class BookLoan(models.Model):
    user = models.ForeignKey(
        way(USERS, USER),
        on_delete=models.CASCADE,
    )
    copy = models.ForeignKey(
        way(BOOKS, COPY),
        on_delete=models.CASCADE,
    )
    load_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(
        # default=datetime.datetime.now().date() + datetime.timedelta(days=LoanDays.week)
    )
    returned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # TODO tentar remover is active

    def __repr__(self) -> str:
        return repr_default(
            BOOK_LOAN,
            self.pk,
            f"{self.copy.book.name}({self.copy.pk}) loan by {self.user}",
        )


class Copy(models.Model):
    book = models.ForeignKey(
        way(BOOKS, BOOK), on_delete=models.CASCADE, related_name="copies"
    )
    is_avaliable = models.BooleanField(default=True)

    def __repr__(self) -> str:
        return repr_default(COPY, self.pk, self.book.name)
