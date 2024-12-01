from django.urls import path, include

urlpatterns = [
    path('foods/', include("apps.foods.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
    path('baskets/', include("apps.baskets.urls")),
    path('categories/', include("apps.categories.urls")),
    path('orders/', include("apps.orders.urls")),
    # path('message/', MessageAPIView.as_view(), name='message-api'),
]
