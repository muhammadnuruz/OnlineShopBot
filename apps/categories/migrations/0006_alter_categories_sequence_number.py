# Generated by Django 5.1.3 on 2024-12-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_categories_sequence_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='sequence_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Кетма-кетлик'),
        ),
    ]
