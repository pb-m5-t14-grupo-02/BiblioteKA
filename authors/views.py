from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Author
from .serializers import AuthorSerializer

class AuthorListCreateView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # TODO: Fazer as classes necessárias do IsStaffOrReadOnly
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [classe IsStaffOrReadOnly]

class AuthorSpecificView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_url_kwarg = "author_id"
    # TODO: Fazer as classes necessárias do IsStaffOrReadOnly
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [classe IsStaffOrReadOnly]
