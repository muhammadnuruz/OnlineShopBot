from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'status', 'total_price', 'ordered_at', 'get_food_items_display',
        'delivery_address', 'payment_status'
    )
    readonly_fields = (
        'ordered_at', 'delivered_at', 'payment_date', 'cancelled_at',
        'confirmed_at', 'created_at', 'updated_at', 'get_food_items_display'
    )
    fieldsets = (
        (None, {
            'fields': (
                'user', 'status', 'total_price', 'delivery_address',
                'latitude', 'longitude', 'note', 'delivery_time', 'get_food_items_display'
            )
        }),
        ('Payment Info', {
            'fields': ('payment_method', 'payment_status', 'payment_date',
                       'payment_confirmed'),
        }),
        ('Dates', {
            'fields': ('ordered_at', 'delivered_at',
                       'cancelled_at', 'confirmed_at', 'created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Food Items')  # Ustun nomini belgilash
    def get_food_items_display(self, obj):
        if not obj.food_items:
            return "No food items"
        items = [
            f"<li>{item['name']} — {item['price']}</li>"
            for item in obj.food_items
        ]
        return format_html("<ul>{}</ul>", "".join(items))
