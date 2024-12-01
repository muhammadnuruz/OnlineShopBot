from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.telegram_users.models import TelegramUsers
from apps.telegram_users.serializers import TelegramUsersSerializer, TelegramUsersCreateSerializer


class TelegramUsersListViewSet(ListAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]


class TelegramUsersCreateViewSet(CreateAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersCreateSerializer
    permission_classes = [AllowAny]


class TelegramUsersUpdateViewSet(UpdateAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersCreateSerializer
    permission_classes = [AllowAny]


class TelegramUsersChatIdDetailViewSet(RetrieveAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        chat_id = self.kwargs.get('chat_id')
        return get_object_or_404(TelegramUsers, chat_id=chat_id)


class TelegramUsersDetailViewSet(RetrieveAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]
