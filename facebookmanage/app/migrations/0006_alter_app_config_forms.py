# Generated by Django 5.1.1 on 2024-10-25 16:06

import utils.encoders
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_appcomment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='config_forms',
            field=models.JSONField(blank=True, default=list, encoder=utils.encoders.PrettyJSONEncoder, null=True),
        ),
    ]
