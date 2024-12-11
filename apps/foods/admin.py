from django.contrib import admin
from apps.foods.models import Foods


class FoodsAdmin(admin.ModelAdmin):
    list_display = (
        'sequence_number', 'name', 'price', 'category', 'compound', 'weight', 'article', 'description', 'created_at'
    )
    ordering = ('sequence_number',)
    list_editable = ('sequence_number',)  # Tahrirlanadigan maydon
    list_display_links = ('name',)  # Bog'lanish uchun maydon (ulanish uchun)
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(Foods, FoodsAdmin)
