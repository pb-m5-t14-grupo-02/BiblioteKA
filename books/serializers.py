from rest_framework import serializers
from .models import Book, BookLoan, Copy, BookFollowing
from users.serializers import UserSerializer, UserSerializerMinimum
from core.constrains import (
    ID,
    IMAGE,
    NAME,
    SERIES,
    GENRE,
    ABOUT,
    YEAR,
    COPIES_COUNT,
    ISBN,
    ASIN,
    LOAD_DATE,
    RETURN_DATE,
    WRITE_ONLY,
    DAYS,
    COPY,
    USER,
    AUTHOR,
    BOOK,
    RETURNED,
)
import datetime
from django.shortcuts import get_object_or_404


class BookSerializer(serializers.ModelSerializer):
    copies_count = serializers.IntegerField(write_only=True)

    def create(self, validated_data: dict):
        copies_counts = validated_data.pop(COPIES_COUNT)
        create_book = Book.objects.create(**validated_data)
        for i in range(copies_counts):
            Copy.objects.create(book=create_book)
        return create_book

    class Meta:
        model = Book
        fields = [
            ID,
            IMAGE,
            NAME,
            SERIES,
            GENRE,
            ABOUT,
            YEAR,
            ISBN,
            ASIN,
            COPIES_COUNT,
            DAYS,
            AUTHOR.lower(),
        ]
        extra_kwargs = {COPIES_COUNT: WRITE_ONLY}
        depth = 1


class BookFollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    def create(self, validated_data):
        return BookFollowing.objects.create(**validated_data)

    class Meta:
        model = BookFollowing
        fields = [USER.lower(), BOOK.lower()]


class BookLoanSerializer(serializers.ModelSerializer):
    user = UserSerializerMinimum(required=False)

    def create(self, validated_data):
        days = validated_data.pop(DAYS)
        return BookLoan.objects.create(**validated_data)

    class Meta:
        depth = 3
        model = BookLoan
        fields = [ID, LOAD_DATE, RETURN_DATE, RETURNED, COPY.lower(), USER.lower()]
        read_only_fields = [RETURN_DATE, LOAD_DATE]
