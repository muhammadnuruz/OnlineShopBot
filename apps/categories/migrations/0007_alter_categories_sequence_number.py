# Generated by Django 5.1.3 on 2024-12-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_alter_categories_sequence_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='sequence_number',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Кетма-кетлик'),
        ),
    ]
