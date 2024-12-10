# Generated by Django 5.1.3 on 2024-12-10 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_final_price'),
        ('telegram_users', '0003_alter_telegramusers_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата отмены'),
        ),
        migrations.AlterField(
            model_name='order',
            name='confirmed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата подтверждения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=255, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='food_items',
            field=models.JSONField(verbose_name='Продукты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_confirmed',
            field=models.BooleanField(default=False, verbose_name='Оплата подтверждена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(max_length=20, verbose_name='Статус оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('kutilmoqda', 'Kutilmoqda'), ('jarayonda', 'Jarayonda'), ('yetkazib berildi', 'Yetkazib berildi'), ('bekor qilingan', 'Bekor qilingan')], default='kutilmoqda', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.FloatField(verbose_name='Общая цена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='telegram_users.telegramusers', verbose_name='Пользователь'),
        ),
    ]