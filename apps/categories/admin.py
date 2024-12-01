from django.contrib import admin

from apps.categories.models import Categories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('created_at',)


admin.site.register(Categories, CategoriesAdmin)
