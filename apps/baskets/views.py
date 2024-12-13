from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

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


class BasketDeleteViewSet(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, food_id, user_id):
        basket = Baskets.objects.filter(food_id=food_id, user_id=user_id).first()

        if not basket:
            return Response({"detail": "Basket not found."}, status=status.HTTP_404_NOT_FOUND)

        basket.delete()

        return Response({"detail": "Basket successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


class BasketDeleteAllViewSet(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, user_id):
        baskets = Baskets.objects.filter(user_id=user_id)

        if not baskets.exists():
            return Response({"detail": "No baskets found for this user."}, status=status.HTTP_404_NOT_FOUND)

        baskets.delete()

        return Response({"detail": "All baskets successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
