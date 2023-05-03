from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from core.constrains import (
    USERNAME,
    EMAIL,
    PASSWORD,
    IS_SUPERUSER,
    IS_COLABORATOR,
    IS_STUDENT,
)


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        user = validated_data.pop("user")
        is_superuser = validated_data.pop("is_superuser")

        if user.is_superuser and is_superuser:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if validated_data.get("password", None):
            password = validated_data.pop("password")
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "is_student",
            "is_colaborator",
            "is_superuser",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [UniqueValidator(queryset=User.objects.all())]},
        }
