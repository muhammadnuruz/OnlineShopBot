from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название (англ.)")
    ru_name = models.CharField(max_length=100, verbose_name="Название (рус.)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
