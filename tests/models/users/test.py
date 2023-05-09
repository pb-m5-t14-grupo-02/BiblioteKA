import ipdb
from django.test import TestCase
from users.models import User
from django.utils.crypto import get_random_string
from tests.models.common import create_user_data
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
import ipdb


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
        self.validate_fields_content(self.adm_instance, self.adm_data)

    def test_user_student_fields(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields_content(self.student_instance, self.student_data)

    def test_user_worker_fields(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields_content(self.worker_instance, self.worker_data)

    def test_if_raise_error_when_invalid_types_fields(self):
        """Test if raise an error when using a invalid type"""
        invalid_user = create_user_data("1212", get_random_string(5), 1234)
        with self.assertRaises(TypeError):
            print(invalid_user)
            User.objects.create_user(**invalid_user)

    def validate_fields_content(self, instance, data):
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



