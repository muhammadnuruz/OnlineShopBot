# Generated by Django 5.1.3 on 2024-12-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0003_alter_telegramusers_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='telegramusers',
            options={'verbose_name': 'Пользователь Telegram', 'verbose_name_plural': 'Пользователи Telegram'},
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='chat_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='Chat ID'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date Created'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='language',
            field=models.CharField(choices=[('ru', 'Ru'), ('uz', 'Uz')], default='uz', max_length=2, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='location',
            field=models.CharField(max_length=255, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='phone_number',
            field=models.CharField(max_length=50, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Date Updated'),
        ),
        migrations.AlterField(
            model_name='telegramusers',
            name='username',
            field=models.CharField(max_length=255, null=True, verbose_name='Username'),
        ),
    ]