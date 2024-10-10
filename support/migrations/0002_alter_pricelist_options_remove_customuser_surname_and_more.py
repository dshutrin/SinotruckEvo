# Generated by Django 5.1.1 on 2024-10-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'verbose_name': 'Прайс-лист', 'verbose_name_plural': 'Прайс-листы'},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='surname',
        ),
        migrations.AddField(
            model_name='customuser',
            name='manager_task',
            field=models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='Задача менеджера'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=12, null=True, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=None, max_length=150, null=True, verbose_name='ФИО/Название организации'),
        ),
    ]