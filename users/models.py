from django.db import models
from django.contrib.auth.models import AbstractUser
from core.constrains import BOOKS, COPY, BOOK_LOAN, USER, repr_default, way
from users.avatar import get_random_avatar


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=True)
    is_colaborator = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_superuser = models.BooleanField(null=True, default=False)
    image = models.FileField(upload_to='users', default=get_random_avatar)
    

    book_loan = models.ManyToManyField(
        way(BOOKS, COPY), through=way(BOOKS, BOOK_LOAN), related_name="copies"
    )

    def __repr__(self) -> str:
        return repr_default(USER, self.pk, self.username)
