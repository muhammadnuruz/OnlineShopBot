from apps.baskets.models import Baskets
from rest_framework import serializers


class BasketsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Baskets
        fields = '__all__'

class BasketsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Baskets
        exclude = ["created_at", "updated_at"]