from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("book/", views.BookView.as_view()),
    path("book/loan/<int:book_id>/", views.BookLoanView.as_view()),
    path("users/loan/<int:user_id>/", views.UserBooksLoan.as_view()),
]
