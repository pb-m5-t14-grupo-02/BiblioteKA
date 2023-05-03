from django.urls import path
from .views import AuthorListCreateView, AuthorSpecificView

urlpatterns = [
    path("authors/", AuthorListCreateView.as_view()),
    path("authors/<int:author_id>/", AuthorSpecificView.as_view())
]
