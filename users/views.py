from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .permissions import IsAccountOwner, IsColaborator, IsSuperuser
from books.models import BookLoan
from books.serializers import BookLoanSerializer


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer: UserSerializer) -> None:
        serializer.save(user=self.request.user)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator or IsSuperuser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner or IsSuperuser]
    lookup_url_kwarg = "user_id"
