# Generated by Django 5.1.7 on 2025-03-28 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_rename_worker_task_executor_alter_task_label'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='label',
            new_name='labels',
        ),
    ]
