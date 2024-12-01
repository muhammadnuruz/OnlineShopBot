from django.db import models

from apps.categories.models import Categories


class Foods(models.Model):
    name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='foods')
    image = models.FileField(upload_to='static/img/')
    description = models.TextField()
    ru_description = models.TextField()
    en_description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"

    def __str__(self):
        return self.name
