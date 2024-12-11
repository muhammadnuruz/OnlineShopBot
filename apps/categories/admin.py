from django.contrib import admin
from apps.categories.models import Categories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('sequence_number', 'name', 'created_at')
    ordering = ('sequence_number',)
    list_editable = ('sequence_number',)  # Tahrirlanadigan maydon
    list_display_links = ('name',)  # Bog'lanish uchun maydon
    list_filter = ('created_at',)
    search_fields = ('name',)


admin.site.register(Categories, CategoriesAdmin)
