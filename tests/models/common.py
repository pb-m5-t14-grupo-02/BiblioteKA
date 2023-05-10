ENDPOINT_EMAIL = "@mail.com"
from core.constrains import IS_SUPERUSER, IS_COLABORATOR, IS_STUDENT, EMAIL, PASSWORD, USERNAME


def create_user_data(username, email, password="1234", is_colaborator=False, is_student=False, is_superuser=False) -> dict:
    return {
        USERNAME: username,
        PASSWORD: password,
        EMAIL: email + ENDPOINT_EMAIL,
        IS_COLABORATOR: is_colaborator,
        IS_STUDENT: is_student,
        IS_SUPERUSER: is_superuser
    }
