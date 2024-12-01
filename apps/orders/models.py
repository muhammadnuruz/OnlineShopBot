from django.db import models

from apps.telegram_users.models import TelegramUsers

class Order(models.Model):
    STATUS_CHOICES = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('jarayonda', 'Jarayonda'),
        ('yetkazib berildi', 'Yetkazib berildi'),
        ('bekor qilingan', 'Bekor qilingan'),
    ]

    user = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE, related_name='orders')
    food_items = models.JSONField()
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='kutilmoqda')
    delivery_address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    payment_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    payment_confirmed = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} by {self.user.name} - {self.status}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"