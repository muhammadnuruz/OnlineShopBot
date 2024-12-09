from django.urls import path

from apps.foods.views import FoodsListViewSet, FoodsSearchAPIView

urlpatterns = [
    path('', FoodsListViewSet.as_view(),
         name='foods-list'),
    path('id/<int:id>/', FoodsSearchAPIView.as_view(), name='food-search-by-id'),
    path('<str:name>/', FoodsSearchAPIView.as_view(), name='food-search'),
]
