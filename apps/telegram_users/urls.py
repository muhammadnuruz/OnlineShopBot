from django.urls import path

from apps.telegram_users.views import TelegramUsersDetailViewSet, TelegramUsersChatIdDetailViewSet, \
    TelegramUsersUpdateViewSet, TelegramUsersCreateViewSet, TelegramUsersListViewSet

urlpatterns = [
    path('', TelegramUsersListViewSet.as_view(),
         name='telegram-users-list'),
    path('create/', TelegramUsersCreateViewSet.as_view(),
         name='telegram-users-create'),
    path('chat_id/<str:chat_id>/', TelegramUsersChatIdDetailViewSet.as_view(),
         name='telegram-users-chat_id'),
    path('detail/<int:pk>/', TelegramUsersDetailViewSet.as_view(),
         name='telegram-users-detail'),
    path('update/<int:pk>/', TelegramUsersUpdateViewSet.as_view(),
         name='telegram-users-update')
]
