from django.db import models

from apps.foods.models import Foods
from apps.telegram_users.models import TelegramUsers


class Baskets(models.Model):
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, related_name='baskets')
    user = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE, related_name='baskets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    def __str__(self):
        return f"{self.user.full_name} - {self.food.name}"
