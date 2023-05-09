from core.constrains import IS_SUPERUSER, IS_COLABORATOR, IS_STUDENT, IS_SUSPENDED, EMAIL, PASSWORD, USERNAME, IMAGE
from django.utils.crypto import get_random_string as grs


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
