# Generated by Django 5.1.3 on 2024-12-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_categories_options_alter_categories_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название (узб.)'),
        ),
    ]
