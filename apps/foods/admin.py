from django.contrib import admin
from apps.foods.models import Foods


class FoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    ordering = ('created_at',)
    list_filter = ('category',)


admin.site.register(Foods, FoodsAdmin)
