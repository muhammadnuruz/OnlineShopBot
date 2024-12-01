from django.db.models import Q
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.foods.models import Foods
from apps.foods.serializers import FoodsSerializer


class FoodsListViewSet(ListAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            return Foods.objects.filter(
                Q(category__name=category) |
                Q(category__ru_name=category) |
                Q(category__en_name=category)
            )
        return Foods.objects.all()


class FoodsDetailViewSet(RetrieveAPIView):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer
    permission_classes = [AllowAny]
