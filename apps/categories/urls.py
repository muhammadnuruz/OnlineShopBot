from django.urls import path

from apps.categories.views import CategoriesListViewSet

urlpatterns = [
    path('', CategoriesListViewSet.as_view(),
         name='categories-list'),
]
