from django.urls import path
from .views import (
    BasketListViewSet,
    BasketCreateViewSet,
    BasketDeleteViewSet, BasketDeleteAllViewSet,
)

urlpatterns = [
    path('create/', BasketCreateViewSet.as_view(), name='basket_create'),
    path('<str:chat_id>/', BasketListViewSet.as_view(), name='basket_list'),
    path('delete/<int:food_id>/<int:user_id>/', BasketDeleteViewSet.as_view(), name='basket_delete'),
    path('delete_all_baskets/<int:user_id>/', BasketDeleteAllViewSet.as_view(), name='delete_all_baskets'),
]
