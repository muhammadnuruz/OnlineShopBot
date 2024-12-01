from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.users.models import User
from apps.users.permissions import UserPermission
from apps.users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, UserRetrieveSerializer


class UserCreateViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDeleteViewSet(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.delete()


class UserUpdateViewSet(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [UserPermission]

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [UserPermission]

    def get_object(self):
        return self.queryset.get(username=self.request.user.username)
