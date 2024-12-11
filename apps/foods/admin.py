from django.contrib import admin
from apps.foods.models import Foods


class FoodsAdmin(admin.ModelAdmin):
    list_display = ('id_display', 'name', 'price', 'category', 'description', 'created_at')
    ordering = ('created_at',)
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def id_display(self, obj):
        return obj.id
    id_display.short_description = "Место"

admin.site.register(Foods, FoodsAdmin)
