# Generated by Django 5.1.1 on 2024-11-07 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_productinorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='Статус заказа'),
        ),
    ]
