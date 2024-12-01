from django.contrib import admin

from apps.baskets.models import Baskets


@admin.register(Baskets)
class BasketsAdmin(admin.ModelAdmin):
    # Ko'rinishda ko'rsatiladigan ustunlar
    list_display = ('get_food_name', 'get_user_name', 'created_at', 'updated_at')
    # Tartarib berish
    ordering = ('food__name', 'user__full_name', 'created_at')
    # Qidiruv maydonlari
    search_fields = ('food__name', 'user__full_name')
    # Filtrlar
    list_filter = ('created_at', 'updated_at')

    # Maxsus ko'rsatish usullari
    @admin.display(description='Food Name')
    def get_food_name(self, obj):
        return obj.food.name

    @admin.display(description='User Name')
    def get_user_name(self, obj):
        return obj.user.full_name  # `user.name` o'rniga `full_name` ishlatildi (to'g'ri maydon ismi bo'lsa).
