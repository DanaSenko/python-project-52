# Generated by Django 5.1.7 on 2025-03-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
