from django.urls import path
from .views import (
    BasketListViewSet,
    BasketCreateViewSet,
    BasketDeleteViewSet,
)

urlpatterns = [
    path('<str:chat_id>/', BasketListViewSet.as_view(), name='basket_list'),
    path('create/', BasketCreateViewSet.as_view(), name='basket_create'),
    path('delete/<int:pk>/', BasketDeleteViewSet.as_view(), name='basket_delete'),
]
