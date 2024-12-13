import random

from django.db import models
import os
import uuid
from apps.categories.models import Categories


class Foods(models.Model):
    sequence_number = models.CharField(
        max_length=5,
        verbose_name="Кетма-кетлик",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100, verbose_name="Название (узб.)")
    ru_name = models.CharField(max_length=100, verbose_name="Название (рус.)")
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='foods',
        verbose_name="Категория"
    )
    image = models.FileField(upload_to='static/img/', verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание (узб.)")
    ru_description = models.TextField(verbose_name="Описание (рус.)")
    compound = models.TextField(verbose_name="Состав (узб.)")
    ru_compound = models.TextField(verbose_name="Состав (рус.)")
    weight = models.CharField(max_length=20, verbose_name="Вес")
    article = models.IntegerField(verbose_name="Артикул")
    price = models.CharField(max_length=20, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.startswith("static/img/"):
            ext = os.path.splitext(self.image.name)[-1]
            random_number = random.randint(0, 10000000000)  # 10 xonali tasodifiy son
            self.image.name = f"{random_number}{ext}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Еда"
        verbose_name_plural = "Еда"

    def __str__(self):
        return self.name
