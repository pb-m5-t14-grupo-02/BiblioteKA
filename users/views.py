from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .permissions import IsAccountOwner, IsColaborator


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
    permission_classes = [IsColaborator]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]
    lookup_field = "pk"
