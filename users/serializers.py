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
            user_created = User.objects.create_superuser(**validated_data)
        else:
            user_created = User.objects.create_user(**validated_data)
        self.send_mail(user_created.email, user_created.username)
        return user_created

    def update(self, instance: User, validated_data: dict) -> User:
        is_admin = validated_data.pop("is_admin")
        if not is_admin:
            forbidden_keys_to_student_update = (IS_SUSPENDED, IS_STUDENT, IS_SUPERUSER, IS_COLABORATOR)
            for key in forbidden_keys_to_student_update:
                if key in validated_data.keys():
                    validated_data.pop(key)
        if validated_data.get(PASSWORD, None):
            password = validated_data.pop(PASSWORD)
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def send_mail(self, email, username):
        import dotenv
        import os
        from .email_template import html_content, text_content
        from django.core.mail import EmailMultiAlternatives
        dotenv.load_dotenv()
        sender = os.getenv("EMAIL_HOST_USER")
        subject = "Bem-vindo a nossa biblioteca"
        msg = EmailMultiAlternatives(
            subject,
            text_content.replace("$username", username),
            sender,
            [email]
        )
        msg.attach_alternative(
            html_content.replace("$username", username),
            "text/html"
        )
        msg.send(fail_silently=True)


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
