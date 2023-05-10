from django.utils.crypto import get_random_string as grs
from random import randint, choice
from core.constrains import (
    IS_SUPERUSER, IS_COLABORATOR, IS_STUDENT,  IS_SUSPENDED, EMAIL, PASSWORD, USERNAME, IMAGE, NAME,
    SERIES, GENRE, ABOUT, YEAR, DAYS, ISBN, ASIN, AUTHOR
)


def create_user_data(
        username=grs(5),
        email=grs(5),
        password="1234",
        is_suspended=False,
        is_colaborator=False,
        is_student=False,
        is_superuser=False
) -> dict:
    ENDPOINT_EMAIL = "@mail.com"
    return {
        USERNAME: username,
        PASSWORD: password,
        EMAIL: email if "@" in email else email + ENDPOINT_EMAIL,
        IS_COLABORATOR: is_colaborator,
        IS_STUDENT: is_student,
        IS_SUPERUSER: is_superuser,
        IS_SUSPENDED: is_suspended,
        IMAGE: "https://bit.ly/41kXJ59"
    }

def create_author_data(
        name=grs(5),
        about=grs(20),
        image="https://bit.ly/44MGxsb"
) -> dict:
    return {
        NAME: name,
        ABOUT: about,
        IMAGE: image
    }


options_loan_days = [7, 15, 30]
def create_book_data(
        author=None,
        name=grs(5),
        series=grs(5),
        genre=grs(5),
        about=grs(20),
        year=randint(1600, 2020),
        days=choice(options_loan_days),
        isbn=grs(13),
        image="https://bit.ly/3McVSuJ",
        asin=grs(10)
) -> dict:
    return {
        NAME: name,
        SERIES: series,
        GENRE: genre,
        ABOUT: about,
        YEAR: year,
        DAYS: days,
        ISBN: isbn,
        ASIN: asin,
        IMAGE: image,
        AUTHOR.lower(): author
    }

