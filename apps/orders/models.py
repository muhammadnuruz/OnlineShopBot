from django.db import models
from apps.telegram_users.models import TelegramUsers


class Order(models.Model):
    STATUS_CHOICES = [
        ('готовится', 'готовится'),
        ('доставляется', 'доставляется'),
        ('доставленный', 'доставленный'),
        ('отменен', 'отменен'),
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
        default='готовится',
        verbose_name="Статус"
    )
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    latitude = models.FloatField(null=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, verbose_name="Долгота")
    note = models.TextField(null=True, blank=True, verbose_name="Описание")
    delivery_time = models.DateTimeField(null=True, blank=True, verbose_name="Время доставки")
    payment_confirmed = models.BooleanField(default=False, verbose_name="Оплата подтверждена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Order {self.pk} by {self.user.full_name} - {self.status}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
