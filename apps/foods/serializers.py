from rest_framework import serializers
from .models import Foods


class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
