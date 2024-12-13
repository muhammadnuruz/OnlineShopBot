from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'status', 'total_price', 'get_food_items_display',
        'delivery_address', "payment_confirmed"
    )
    readonly_fields = (
        'created_at', 'updated_at', 'get_food_items_display'
    )
    fieldsets = (
        (None, {
            'fields': (
                'user', 'status', 'total_price', 'delivery_address',
                'latitude', 'longitude', 'note', 'delivery_time', 'get_food_items_display'
            )
        }),
        ('Payment Info', {
            'fields': ('payment_confirmed',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Продукты питания')
    def get_food_items_display(self, obj):
        if not obj.food_items:
            return "No food items"

        items = []
        for item in obj.food_items:
            food_name = item.get('food_name', 'No Name')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)

            items.append(f"<li>{food_name} — {quantity} pcs — {price} UZS</li>")

        return mark_safe(f"<ul>{''.join(items)}</ul>")
