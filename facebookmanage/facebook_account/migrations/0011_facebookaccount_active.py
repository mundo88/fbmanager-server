# Generated by Django 5.1.1 on 2024-10-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_account', '0010_alter_facebookaccount_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookaccount',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
