from django.test import TestCase
from django.db.models.fields.files import FieldFile
from django.db.utils import IntegrityError
from random import random
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from users.models import User
from django.utils.crypto import get_random_string as grs
from tests.models.common import create_user_data
from core.constrains import (
    IS_SUPERUSER,
    IS_COLABORATOR,
    IS_STUDENT,
    IS_SUSPENDED,
    EMAIL,
    IMAGE,
    PASSWORD,
    USERNAME,
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

    def test_fields_are_the_same_from_different_types_of_users(self):
        """Testing if all model fields are correctly added to database"""
        self.validate_fields_content(self.adm_instance, self.adm_data)
        self.validate_fields_content(self.student_instance, self.student_data)
        self.validate_fields_content(self.worker_instance, self.worker_data)

    def test_verify_types_fields_content(self):
        """Test if types of fields are correctly"""
        string_fields = (PASSWORD, USERNAME, EMAIL)
        expected = str
        for field in string_fields:
            result = type(getattr(self.adm_instance, field))
            self.assertEqual(result, expected)

        bool_fields = (IS_SUSPENDED, IS_COLABORATOR, IS_STUDENT, IS_SUPERUSER)
        expected = bool
        for field in bool_fields:
            result = type(getattr(self.adm_instance, field))
            self.assertEqual(result, expected)

        result = type(self.adm_instance.image)
        expected = FieldFile
        self.assertEqual(result, expected)

    def test_if_raise_error_when_invalid_types_fields(self):
        """Test if raise an error when using a invalid type"""
        invalid_user = create_user_data("invalid", grs(5), random())
        with self.assertRaises(TypeError):
            User.objects.create_user(**invalid_user)

        invalid_user[PASSWORD] = grs(5)
        invalid_user[IS_SUPERUSER] = grs(5)
        with self.assertRaises(ValidationError):
            User.objects.create_user(**invalid_user)

        invalid_user[IS_STUDENT] = grs(5)
        with self.assertRaises(ValidationError):
            User.objects.create_user(**invalid_user)

        invalid_user[IS_STUDENT] = True
        invalid_user[IS_COLABORATOR] = random()
        with self.assertRaises(ValidationError):
            User.objects.create_user(**invalid_user)

        invalid_user[IS_COLABORATOR] = True
        invalid_user[EMAIL] = grs(5)
        with self.assertRaises(ValidationError):
            validate_email(invalid_user[EMAIL])

    def test_if_raise_error_when_email_already_in_use(self):
        """Test if cannot create with email that is already in use"""
        user_data = create_user_data(email=self.adm_instance.email)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user_data)

    def test_if_raise_error_when_username_already_in_use(self):
        """Test if cannot create with username that is already in use"""
        user_data = create_user_data(username=self.adm_instance.username)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**user_data)

    def test_fields_max_length(self):
        """Test if the max length of this fields is right"""
        result = self.adm_instance._meta.get_field(USERNAME).max_length
        expected = 150
        self.assertEqual(result, expected)

        result = self.adm_instance._meta.get_field(EMAIL).max_length
        expected = 254
        self.assertEqual(result, expected)

        result = self.adm_instance._meta.get_field(PASSWORD).max_length
        expected = 128
        self.assertEqual(result, expected)

    def validate_fields_content(self, instance, data):
        fields = (USERNAME, EMAIL, IS_SUPERUSER, IS_COLABORATOR, IS_SUSPENDED, IS_STUDENT, IMAGE)
        for field in fields:
            result = getattr(instance, field)
            expected = data[field]
            msg = f"Checking if {field} is the same"
            self.assertEqual(result, expected, msg)

        result = instance.password
        expected = data[PASSWORD]
        msg = "Checking if password is hashed"
        self.assertNotEqual(result, expected, msg)

        result = instance.check_password(data[PASSWORD])
        msg = "Checking if the password is hashed correctly"
        self.assertTrue(result, msg)





