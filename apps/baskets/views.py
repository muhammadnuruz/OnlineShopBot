from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from .models import Baskets
from .serializers import BasketsSerializer, BasketsCreateSerializer
from ..telegram_users.models import TelegramUsers


class BasketListViewSet(ListAPIView):
    serializer_class = BasketsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        return Baskets.objects.filter(user=user)


class BasketCreateViewSet(CreateAPIView):
    queryset = Baskets.objects.all()
    serializer_class = BasketsCreateSerializer
    permission_classes = [AllowAny]


class BasketDeleteViewSet(DestroyAPIView):
    queryset = Baskets.objects.all()
    serializer_class = BasketsSerializer
    permission_classes = [AllowAny]
