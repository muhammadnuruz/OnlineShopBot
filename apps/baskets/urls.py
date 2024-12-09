from django.urls import path
from .views import (
    BasketListViewSet,
    BasketCreateViewSet,
    BasketDeleteViewSet,
)

urlpatterns = [
    path('create/', BasketCreateViewSet.as_view(), name='basket_create'),
    path('<str:chat_id>/', BasketListViewSet.as_view(), name='basket_list'),
    path('delete/<int:pk>/', BasketDeleteViewSet.as_view(), name='basket_delete'),
]
