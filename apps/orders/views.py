from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer, OrderCreateSerializer
from apps.telegram_users.models import TelegramUsers


class OrderListViewSet(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        user = get_object_or_404(TelegramUsers, chat_id=chat_id)
        return Order.objects.filter(user=user)


class OrderCreateViewSet(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [AllowAny]
