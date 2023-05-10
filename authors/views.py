from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Author
from .serializers import AuthorSerializer
from users.permissions import IsSuperuser, IsColaborator, ReadOnly


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ReadOnly | IsColaborator | IsSuperuser]


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = "author_id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperuser | IsColaborator | IsSuperuser]
