from rest_framework import serializers
from .models import Book, BookLoan, Copy
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
    IS_ACTIVE,
    WRITE_ONLY,
    DAYS,
    COPY,
)
import datetime
import ipdb


class BookSerializer(serializers.ModelSerializer):
    copies_count = serializers.IntegerField(write_only=True)

    def create(self, validated_data: dict):
        # from ipdb import set_trace
        # set_trace()


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
            "author",
        ]
        extra_kwargs = {COPIES_COUNT: WRITE_ONLY}
        depth = 1


class BookLoanSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        days = validated_data.pop("days")
        initial_date = datetime.datetime.now()
        end_date = initial_date + datetime.timedelta(days=days)
        validated_data["return_date"] = end_date.date()
        return BookLoan.objects.create(**validated_data)

    class Meta:
        depth = 3
        model = BookLoan
        fields = [ID, LOAD_DATE, RETURN_DATE, IS_ACTIVE, COPY.lower()]
        read_only_fields = [RETURN_DATE, LOAD_DATE]
