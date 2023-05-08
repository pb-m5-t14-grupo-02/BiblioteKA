from django.urls import path
from .views import AuthorListCreateView, AuthorDetailView

urlpatterns = [
    path("authors/", AuthorListCreateView.as_view()),
    path("authors/<int:author_id>/", AuthorDetailView.as_view()),
]
