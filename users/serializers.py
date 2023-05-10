from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from core.constrains import (
    ID,
    USERNAME,
    EMAIL,
    PASSWORD,
    IS_SUPERUSER,
    IS_COLABORATOR,
    IS_STUDENT,
    WRITE_ONLY,
    VALIDATORS,
    IMAGE,
    IS_SUSPENDED,
    USER
)


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        user = validated_data.pop(USER.lower())

        if user.is_superuser and validated_data[IS_SUPERUSER]:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if validated_data.get(PASSWORD, None):
            password = validated_data.pop(PASSWORD)
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            ID,
            USERNAME,
            EMAIL,
            IMAGE,
            PASSWORD,
            IS_STUDENT,
            IS_COLABORATOR,
            IS_SUPERUSER,
            IS_SUSPENDED,
        ]
        read_only_fields = [IS_SUSPENDED] # TODO: Talvez precisa trocar
        extra_kwargs = {
            PASSWORD: WRITE_ONLY,
            EMAIL: {VALIDATORS: [UniqueValidator(queryset=User.objects.all())]},
        }


class UserSerializerMinimum(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            ID,
            USERNAME,
            EMAIL,
            IMAGE,
            IS_SUSPENDED,
        ]
