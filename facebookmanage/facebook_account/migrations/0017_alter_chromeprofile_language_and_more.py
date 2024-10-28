# Generated by Django 5.1.1 on 2024-10-20 18:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_account', '0016_alter_chromeprofile_fbaccount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='chromeprofile',
            name='language',
            field=models.CharField(choices=[('en-US', 'Tiếng Anh (Hoa Kỳ)'), ('en-GB', 'Tiếng Anh (Anh)'), ('vi', 'Tiếng Việt'), ('fr', 'Tiếng Pháp'), ('de', 'Tiếng Đức'), ('es', 'Tiếng Tây Ban Nha'), ('zh-CN', 'Tiếng Trung (Giản thể)'), ('zh-TW', 'Tiếng Trung (Phồn thể)'), ('ja', 'Tiếng Nhật'), ('ko', 'Tiếng Hàn'), ('ru', 'Tiếng Nga'), ('pt-BR', 'Tiếng Bồ Đào Nha (Brazil)'), ('it', 'Tiếng Ý'), ('ar', 'Tiếng Ả Rập'), ('th', 'Tiếng Thái'), ('id', 'Tiếng Indonesia'), ('nl', 'Tiếng Hà Lan'), ('el', 'Tiếng Hy Lạp'), ('pl', 'Tiếng Ba Lan')], default='vi', max_length=255, verbose_name='Ngôn ngữ'),
        ),
        migrations.AlterField(
            model_name='facebookaccount',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='fb_accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]
