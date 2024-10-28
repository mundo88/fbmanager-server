from django.db import models



class FacebookAccount(models.Model):
    uid = models.CharField(max_length=255, unique=True,verbose_name='UID')
    password = models.CharField(max_length=255,verbose_name='Mật khẩu')
    _2fa = models.CharField(blank=True, null=True, max_length=255,verbose_name='2FA')
    cookie = models.TextField(default='', blank=True,verbose_name='Cookie')
    access_token = models.CharField(blank=True, null=True,max_length=255,verbose_name='Access Token')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Tên')
    email = models.EmailField(unique=True, blank=True, null=True,verbose_name='Email')
    pass_mail = models.CharField(max_length=255, blank=True, null=True, verbose_name='Mật khẩu email')
    phone_number = models.CharField(max_length=20,blank=True,null=True,verbose_name='Số điện thoại')
    profile_picture = models.TextField(blank=True, null=True,verbose_name='Ảnh đại diện',default='https://bbb.u-pec.fr/assets/default-avatar-12ba46e182bedfae9d6de6c3a414a91b85a2383adff1e06ba4261478c380d3e1.png')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Lần cập nhật cuối')
    last_login = models.DateTimeField(auto_now=True,verbose_name='Lần đăng nhập cuối')
    active = models.BooleanField(default=True,verbose_name='Trạng thái hoạt động')
    collaborators = models.ManyToManyField('account.Account',verbose_name='Cộng tác viên', related_name='fb_accounts', blank=True)
    
    def __str__(self):
        return self.uid
    
class ChromeProfile(models.Model):
    CHROME_LANGUAGE_CHOICES = [
        ('en-US', 'Tiếng Anh (Hoa Kỳ)'),
        ('en-GB', 'Tiếng Anh (Anh)'),
        ('vi', 'Tiếng Việt'),
        ('fr', 'Tiếng Pháp'),
        ('de', 'Tiếng Đức'),
        ('es', 'Tiếng Tây Ban Nha'),
        ('zh-CN', 'Tiếng Trung (Giản thể)'),
        ('zh-TW', 'Tiếng Trung (Phồn thể)'),
        ('ja', 'Tiếng Nhật'),
        ('ko', 'Tiếng Hàn'),
        ('ru', 'Tiếng Nga'),
        ('pt-BR', 'Tiếng Bồ Đào Nha (Brazil)'),
        ('it', 'Tiếng Ý'),
        ('ar', 'Tiếng Ả Rập'),
        ('th', 'Tiếng Thái'),
        ('id', 'Tiếng Indonesia'),
        ('nl', 'Tiếng Hà Lan'),
        ('el', 'Tiếng Hy Lạp'),
        ('pl', 'Tiếng Ba Lan'),
    ]
    CHOMRE_VERSION_CHOICES = [
        ('128', '128'),
        ('127', '127'),
        ('126', '126'),
        ('125', '125'),
        ('124', '124'),
        ('123', '123'),
        ('122', '122'),
        ('121', '121'),
        ('120', '120'),
        ('119', '119'),
        ('118', '118'),
        ('117', '117'),
    ]
    version = models.CharField(max_length=255,default="128",verbose_name='Phiên bản chrome',choices=CHOMRE_VERSION_CHOICES)
    size = models.CharField(max_length=255,default='1024x768',verbose_name='Kích thước cửa sổ')
    language = models.CharField(max_length=255, choices=CHROME_LANGUAGE_CHOICES, default='vi', verbose_name='Ngôn ngữ')
    ua = models.CharField(max_length=255,null=True,blank=True,default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',verbose_name='User Agent')
    start_url = models.CharField(max_length=255,default='https://www.facebook.com',verbose_name='URL mở đầu')
    proxy = models.CharField(max_length=255,blank=True,null=True)
    profile_path = models.CharField(max_length=255,blank=True,null=True,verbose_name='Đường dẫn tới profile')
    lite_mode = models.BooleanField(default=False,verbose_name='Chế độ thu gọn')
    remove_cache_after_run = models.BooleanField(default=False,verbose_name='Xóa bộ nhớ đệm sau khi chạy')
    fbaccount = models.OneToOneField('FacebookAccount', on_delete=models.CASCADE, related_name='chrome_profile')

    def save(self, *args, **kwargs):
        if not self.profile_path:
            self.profile_path = self.fbaccount.uid  # Lấy giá trị uid từ FacebookAccount
        super().save(*args, **kwargs)
