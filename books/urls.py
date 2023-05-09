from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int:book_id>/", views.BookDetailView.as_view()),
    path("books/loan/<int:book_id>/", views.BookLoanView.as_view()),
    path("users/loan/<int:user_id>/", views.UserBooksLoan.as_view()),
]
