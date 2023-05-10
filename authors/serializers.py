from rest_framework import serializers
from .models import Author
from core.constrains import ID, IMAGE, NAME, ABOUT


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [ID, NAME, ABOUT, IMAGE]
        read_only_fields = [ID]
