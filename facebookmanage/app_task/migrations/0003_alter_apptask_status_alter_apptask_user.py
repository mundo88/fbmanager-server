# Generated by Django 5.1.1 on 2024-10-18 04:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_task', '0002_rename_author_apptask_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='apptask',
            name='status',
            field=models.CharField(choices=[('processing', 'Đang chạy'), ('pending', 'Đang chờ'), ('done', 'Hoàn thành'), ('failed', 'Lỗi'), ('canceled', 'Hủy bỏ')], default='pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='apptask',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
