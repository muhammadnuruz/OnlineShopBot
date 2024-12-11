from django.contrib import admin

from apps.categories.models import Categories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('sequence_number', 'name', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    search_fields = ('name',)


admin.site.register(Categories, CategoriesAdmin)
