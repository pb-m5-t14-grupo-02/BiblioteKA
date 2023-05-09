NAME = "name"
IMAGE = "image"
GENRE = "genre"
ABOUT = "about"
YEAR = "year"
COPIES = "copies"
COPY = "Copy"
AUTHORS = "authors"
AUTHOR = "Author"
USERS = "users"
USER = "User"
BOOKS = "books"
BOOK = "Book"
BOOK_LOAN = "BookLoan"
EMAIL = "email"
USERNAME = "username"
LOAN_DATE = "loan_date"
RETURN_DATE = "return_date"
ISBN = "ISBN"
ASIN = "ASIN"
JSON = "json"
ID = "id"
WRITE_ONLY = {"write_only": True}
DEFAULT = "default"
SERIES = "series"
POSTGRES_ = "POSTGRES_"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
PASSWORD = "password"
IS_SUPERUSER = "is_superuser"
IS_COLABORATOR = "is_colaborator"
IS_STUDENT = "is_student"
IS_SUSPENDED = "is_suspended"
IS_ACTIVE = "is_active"
VALIDATORS = "validators"
URLS = "urls"
COPIES_COUNT = "copies_count"
LOAD_DATE = "load_date"
DAYS = "days"



def way(arg1: str, arg2: str) -> str:
    return arg1 + "." + arg2


def repr_default(cls: str, pk: int, field: any) -> str:
    return f"<{cls.capitalize()}: {field} [{pk}]>"
