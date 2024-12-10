from django.db import models
from apps.telegram_users.models import TelegramUsers


class Order(models.Model):
    STATUS_CHOICES = [
        ('kutilmoqda', 'Kutilmoqda'),
        ('jarayonda', 'Jarayonda'),
        ('yetkazib berildi', 'Yetkazib berildi'),
        ('bekor qilingan', 'Bekor qilingan'),
    ]

    user = models.ForeignKey(
        TelegramUsers,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Пользователь"
    )
    food_items = models.JSONField(verbose_name="Продукты")
    total_price = models.FloatField(verbose_name="Общая цена")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='kutilmoqda',
        verbose_name="Статус"
    )
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    latitude = models.FloatField(null=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, verbose_name="Долгота")
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата доставки")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")
    payment_status = models.CharField(max_length=20, verbose_name="Статус оплаты")
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплаты")
    note = models.TextField(null=True, blank=True, verbose_name="Примечания")
    delivery_time = models.DateTimeField(null=True, blank=True, verbose_name="Время доставки")
    payment_confirmed = models.BooleanField(default=False, verbose_name="Оплата подтверждена")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата отмены")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата подтверждения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Order {self.pk} by {self.user.name} - {self.status}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
