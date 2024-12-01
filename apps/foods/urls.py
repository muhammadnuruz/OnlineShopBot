from django.urls import path

from apps.foods.views import FoodsListViewSet, FoodsDetailViewSet

urlpatterns = [
    path('', FoodsListViewSet.as_view(),
         name='foods-list'),
    path('detail/<int:pk>/', FoodsDetailViewSet.as_view(),
         name='foods-detail'),
]
