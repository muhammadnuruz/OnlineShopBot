from django.contrib import admin

from apps.categories.models import Categories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    search_fields = ('name',)

    def id_display(self, obj):
        return obj.id
    id_display.short_description = "Место"


admin.site.register(Categories, CategoriesAdmin)
