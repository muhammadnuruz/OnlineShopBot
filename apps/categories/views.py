from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.categories.models import Categories
from apps.categories.serializers import CategoriesSerializer


class CategoriesListViewSet(ListAPIView):
    queryset = Categories.objects.all().order_by('sequence_number')
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
