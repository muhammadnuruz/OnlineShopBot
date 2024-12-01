from django.urls import path
from .views import OrderListViewSet, OrderCreateViewSet

urlpatterns = [
    path('create/', OrderCreateViewSet.as_view(), name='order-create'),
    path('<str:chat_id>/', OrderListViewSet.as_view(), name='order-list'),
]
