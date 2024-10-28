from django.db import models


class AppTask(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'processing', 'Đang chạy'
        PENDING = 'pending', 'Đang chờ'
        DONE = 'done', 'Hoàn thành'
        FAILED = 'failed', 'Lỗi'
        CANCELED = 'canceled', 'Hủy bỏ'
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING)
    status_text = models.CharField(max_length=255, default='Đang chờ', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fb_accounts = models.ManyToManyField('facebook_account.FacebookAccount', related_name='app_tasks')
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='app_tasks',null=True, blank=True)
    app = models.ForeignKey('app.App', on_delete=models.CASCADE, related_name='app_tasks')
    
    def __str__(self):
        return self.title
