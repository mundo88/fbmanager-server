# Generated by Django 5.1.1 on 2024-10-17 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_account', '0014_rename_remove_cache_chromeprofile_remove_cache_after_run_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chromeprofile',
            name='language',
            field=models.CharField(default='Vietnamese-vi', max_length=255, verbose_name='Ngôn ngữ'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='lite_mode',
            field=models.BooleanField(default=False, verbose_name='Chế độ thu gọn'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='profile_path',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Đường dẫn tới profile'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='remove_cache_after_run',
            field=models.BooleanField(default=False, verbose_name='Xóa bộ nhớ đệm sau khi chạy'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='size',
            field=models.CharField(default='1024x768', max_length=255, verbose_name='Kích thước cửa sổ'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='start_url',
            field=models.CharField(default='https://www.facebook.com', max_length=255, verbose_name='URL mở đầu'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='ua',
            field=models.CharField(blank=True, default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', max_length=255, null=True, verbose_name='User Agent'),
        ),
        migrations.AlterField(
            model_name='chromeprofile',
            name='version',
            field=models.CharField(default='128', max_length=255, verbose_name='Phiên bản chrome'),
        ),
    ]
