# Generated by Django 5.1.1 on 2024-10-10 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0002_alter_pricelist_options_remove_customuser_surname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='file_sharing_delete_document_permission',
            field=models.BooleanField(default=False, verbose_name='Возможность удалять файлы в файлообменнике'),
        ),
    ]
