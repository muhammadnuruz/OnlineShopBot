from rest_framework import serializers

from apps.telegram_users.models import TelegramUsers


class TelegramUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        fields = "__all__"


class TelegramUsersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUsers
        exclude = ['created_at', 'updated_at']
