# Generated by Django 5.1.3 on 2024-12-11 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0006_alter_foods_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='foods',
            name='article',
            field=models.IntegerField(default='1', verbose_name='Артикул'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foods',
            name='weight',
            field=models.IntegerField(default=1, verbose_name='Вес'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foods',
            name='description',
            field=models.TextField(verbose_name='Состав (узб.)'),
        ),
        migrations.AlterField(
            model_name='foods',
            name='ru_description',
            field=models.TextField(verbose_name='Состав (рус.)'),
        ),
    ]