# Generated by Django 5.1.3 on 2024-12-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_order_cancelled_at_remove_order_confirmed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('готовится', 'готовится'), ('доставляется', 'доставляется'), ('доставленный', 'доставленный'), ('отменен', 'отменен')], default='kutilmoqda', max_length=20, verbose_name='Статус'),
        ),
    ]
