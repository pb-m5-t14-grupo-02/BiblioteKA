from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Book, BookLoan, Copy, BookFollowing
from .serializers import BookSerializer, BookLoanSerializer, BookFollowingSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborator, IsSuperuser, IsAccountOwner, ReadOnly
from .permissions import IsSuspended
from users.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from authors.models import Author
from rest_framework.views import Response, status


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnly | IsColaborator | IsSuperuser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        # TODO: ver se existe um modo mais fácil
        author_id = self.request.data.get("author")
        author = get_object_or_404(Author, id=author_id)
        serializer.save(author=author)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnly | IsColaborator | IsSuperuser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"


class BookFollowingView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BookFollowing.objects.all()
    serializer_class = BookFollowingSerializer

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        book_following = BookFollowing.objects.filter(book=book, user=self.request.user).first()
        if book_following:
            return Response({"message": "You already follow this book"} ,status=status.HTTP_409_CONFLICT)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):        
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        serializer.save(book=book, user=self.request.user)
    
    def get_queryset(self):
        get_object_or_404(BookFollowing, id=self.kwargs["book_id"])
        return BookFollowing.objects.filter(user=self.request.user)


class BookDetailView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        find_book = get_object_or_404(Book, id=self.kwargs["book_id"])
        return Book.objects.filter(id=find_book.id)


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
    permission_classes = [IsAccountOwner | IsSuperuser]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            find_user = get_object_or_404(User, id=self.kwargs["user_id"])
            return BookLoan.objects.filter(user=find_user)

        return BookLoan.objects.filter(user=self.request.user)
