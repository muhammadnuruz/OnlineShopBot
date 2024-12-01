from django.contrib import admin
from apps.foods.models import Foods


class FoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_category_name', 'created_at')
    ordering = ('created_at',)

    def get_category_name(self, obj):
        return obj.category.name
    get_category_name.short_description = 'Category'


admin.site.register(Foods, FoodsAdmin)
