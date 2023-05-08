from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Book, BookLoan, Copy
from .serializers import BookSerializer, BookLoanSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborator, IsSuperuser, IsAccountOwner
from .permissions import IsSuspended
from rest_framework.response import Response
from users.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
import ipdb

# from django.contrib.messages.views


class BookView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator or IsSuperuser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookLoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuspended]

    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        copy = get_list_or_404(Copy, book=book, is_avaliable=True)[0]
        copy.is_avaliable = False
        copy.save()
        serializer.save(copy=copy, user=self.request.user, days=copy.book.days)


class UserBooksLoan(generics.ListAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner or IsSuperuser]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            find_user = get_object_or_404(User, id=self.kwargs["user_id"])
            return BookLoan.objects.filter(user=find_user)

        return BookLoan.objects.filter(user=self.request.user)
