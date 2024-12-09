from django.db import models
import os
import uuid
from apps.categories.models import Categories


class Foods(models.Model):
    name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='foods')
    image = models.FileField(upload_to='static/img/')
    description = models.TextField()
    ru_description = models.TextField()
    price = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.startswith("static/img/"):
            ext = os.path.splitext(self.image.name)[-1]
            self.image.name = f"{uuid.uuid4().hex}{ext}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"

    def __str__(self):
        return self.name
