from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Book, BookLoan, Copy, BookFollowing
from .serializers import BookSerializer, BookLoanSerializer, BookFollowingSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsColaborator, IsSuperuser, IsAccountOwner, IsStudent, ReadOnly
from .permissions import IsMyOwnAccountSuspended, IsStudentSuspended
from users.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from datetime import timedelta, datetime
from django.utils import timezone
from authors.models import Author
from core.jobs.tarefa1 import scheduler
import ipdb
from rest_framework.views import Response, status


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnly | IsColaborator | IsSuperuser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
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
            return Response({"message": "You already follow this book"}, status=status.HTTP_409_CONFLICT)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):        
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        serializer.save(book=book, user=self.request.user)
    
    def get_queryset(self):
        get_object_or_404(BookFollowing, id=self.kwargs["book_id"])
        return BookFollowing.objects.filter(user=self.request.user)


class BookColaboratorSelfLoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator | IsSuperuser, IsMyOwnAccountSuspended]
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        copy = get_list_or_404(Copy, book=book, is_avaliable=True)[0]
        copy.is_avaliable = False
        copy.save()

        # Adicionando a data de retorno do livro emprestado
        now = timezone.now()
        due_date = now + timedelta(days=copy.book.days)
        if due_date.weekday() in [5, 6]:  # 5=sábado, 6=domingo
            due_date += timedelta(days=8 - due_date.weekday())
        serializer.save(
            copy=copy,
            user=self.request.user,
            days=copy.book.days,
            due_date=due_date.date(),
        )


class BookColaboratorLoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator | IsSuperuser, IsStudentSuspended]
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    lookup_url_kwarg = ["book_id", "student_id"]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs["book_id"])
        student = get_object_or_404(User, id=self.kwargs["student_id"])
        copy = get_list_or_404(Copy, book=book, is_avaliable=True)[0]
        copy.is_avaliable = False
        copy.save()

        # Adicionando a data de retorno do livro emprestado
        now = timezone.now()
        due_date = now + timedelta(days=copy.book.days)
        if due_date.weekday() in [5, 6]:  # 5=sábado, 6=domingo
            due_date += timedelta(days=8 - due_date.weekday())
        serializer.save(
            copy=copy,
            user=student,
            days=copy.book.days,
            due_date=due_date.date(),
        )


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

    # Verificando se a devolução está atrasada e bloqueia o usuário
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        now = timezone.now()
        for book_loan in queryset:
            if not book_loan.returned and book_loan.return_date < now.date():
                # Bloqueando o usuário que está com empréstimo atrasado
                user = book_loan.user
                user.is_suspended = True
                user.save()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookReturnView(generics.UpdateAPIView):
    lookup_url_kwarg = "book_loan_id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMyOwnAccountSuspended]

    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer

    def perform_update(self, serializer):
        book_loan = serializer.save(returned=True, return_date=timezone.now().date())
        copy = book_loan.copy
        copy.is_avaliable = True
        copy.save()


class AllBooksLoanDelayedList(generics.ListAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        delayed_loans = []
        for book_loan in queryset:
            if not book_loan.returned and (
                book_loan.return_date < timezone.now().date()
            ):
                delayed_loans.append(book_loan)
        serializer = self.get_serializer(delayed_loans, many=True)
        return Response(serializer.data)


class AllBooksLoanList(generics.ListAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]


class AllBooksLoanOnDateList(generics.ListAPIView):
    queryset = BookLoan.objects.all()
    serializer_class = BookLoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ondate_loans = []
        for book_loan in queryset:
            if not book_loan.returned and (
                book_loan.return_date >= timezone.now().date()
            ):
                ondate_loans.append(book_loan)
        serializer = self.get_serializer(ondate_loans, many=True)
        return Response(serializer.data)
