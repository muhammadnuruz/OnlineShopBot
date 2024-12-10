from django.db import models


class TelegramUsers(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Ru'),
        ('uz', 'Uz'),
    ]
    chat_id = models.CharField(max_length=255, unique=True, verbose_name="Идентификатор чата")
    username = models.CharField(max_length=255, null=True, verbose_name="Имя пользователя")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона")
    latitude = models.FloatField(null=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, verbose_name="Longitude")
    location = models.CharField(max_length=255, null=True, verbose_name="Расположение")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='uz', verbose_name="Язык")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return f"{self.full_name}"
