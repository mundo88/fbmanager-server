from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _



    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class AccountSettings(models.Model):
    class ThemeChoice(models.TextChoices):
        SYSTEM = 'system', _('System')
        DARK = 'dark', _('Dark')
        LIGHT = 'light', _('Light')
    max_thread=models.IntegerField(default=5)
    space_time = models.IntegerField(default=10)
    setup_screen = models.BooleanField(default=True)
    unlock_checkpoint = models.BooleanField(default=True)
    update_info = models.BooleanField(default=True)
    tray_icon = models.BooleanField(default=True)
    startup_app = models.BooleanField(default=True)
    lock_screen = models.BooleanField(default=True)
    lock_screen_password = models.CharField(max_length=255,default='',blank=True)
    theme = models.CharField(max_length=255,default='system',choices=ThemeChoice.choices)
    primary_color = models.CharField(max_length=255,default='blue')
    notification = models.BooleanField(default=True)
    notification_preview = models.BooleanField(default=True)
    two_factor_auth = models.BooleanField(default=True)
    user = models.OneToOneField('Account', on_delete=models.CASCADE, related_name='settings',null=True)
    
    def __str__(self):
        return str(self.user)
class Account(AbstractUser):
    # Add additional fields here if needed
    email = models.EmailField(unique=True)
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    name = models.CharField(max_length=255) 
    installed_apps = models.ManyToManyField('app.App', related_name='users_installed',blank=True)
    email = models.EmailField(_('email address'), unique=True) # changes email to unique and blank to false
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    

