from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/following/<int:book_id>/", views.BookFollowingView.as_view()),
    path("books/<int:book_id>/", views.BookDetailView.as_view()),
    path("books/colaborator/self_loan/<int:book_id>/", views.BookColaboratorLoanView.as_view()),
    path("books/colaborator/<int:student_id>/loan/<int:book_id>/", views.BookColaboratorLoanView.as_view()),
    path("users/loan/<int:user_id>/", views.UserBooksLoan.as_view()),
    path("book/return/<int:book_loan_id>/", views.BookReturnView.as_view()),
    path("loans/delayed/", views.AllBooksLoanDelayedList.as_view()),
    path("loans/ondate/", views.AllBooksLoanOnDateList.as_view()),
    path("loans/all/", views.AllBooksLoanList.as_view()),
]
