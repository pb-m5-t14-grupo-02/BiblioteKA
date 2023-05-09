from django.test import TestCase
from users.models import User
from tests.models.common import ENDPOINT_EMAIL, create_user_data
from core.constrains import (
    IS_SUPERUSER,
    IS_COLABORATOR,
    IS_STUDENT,
    IS_ACTIVE,
    IMAGE,
    EMAIL,
    PASSWORD,
    USERNAME
)


class TestModelUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.adm_data = create_user_data("Adminstrator", "admin", is_superuser=True)
        cls.adm_instance = User.objects.create_superuser(**cls.adm_data)

        cls.student_data = create_user_data("Common", "common", is_student=True)
        cls.student_instance = User.objects.create_user(**cls.student_data)

        cls.worker_data = create_user_data("Worker", "work", is_colaborator=True)
        cls.worker_instance = User.objects.create_user(**cls.worker_data)

    def test_user_adm_fields(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields(self.adm_instance, self.adm_data)

    def test_user_student_fields(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields(self.student_instance, self.student_data)

    def test_user_worker_fields(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields(self.worker_instance, self.worker_data)

    def validate_fields(self, instance, data):
        fields = [USERNAME, EMAIL, IS_SUPERUSER, IS_COLABORATOR, IS_STUDENT]
        for field in fields:
            result = getattr(instance, field)
            expected = data[field]
            msg = f'Checking if {field} is the same'
            self.assertEqual(result, expected, msg)

        result = instance.password
        expected = data[PASSWORD]
        msg = 'Checking if password is hashed'
        self.assertNotEqual(result, expected, msg)

        result = instance.check_password(data[PASSWORD])
        msg = 'Checking if the password is hashed correctly'
        self.assertTrue(result, msg)



