from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.foods.models import Foods
from apps.foods.serializers import FoodsSerializer


class FoodsListViewSet(ListAPIView):
    queryset = Foods.objects.all().order_by('sequence_number')
    serializer_class = FoodsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return Foods.objects.filter(
                Q(category__name__icontains=category) |
                Q(category__ru_name__icontains=category)
            )
        return Foods.objects.all()


class FoodsSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        food_id = self.kwargs.get('id')
        food_name = self.kwargs.get('name')

        if food_id:
            food = get_object_or_404(Foods, id=food_id)
        elif food_name:
            food = get_object_or_404(Foods, Q(name=food_name) | Q(ru_name=food_name))
        else:
            return Response({"detail": "ID yoki nom ko'rsatilishi kerak."}, status=400)

        serializer = FoodsSerializer(food)
        return Response(serializer.data)
