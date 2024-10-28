from django.db import models
from utils.encoders import PrettyJSONEncoder

class AppCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class AppTag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class AppChangelog(models.Model):
    class ChangeType(models.TextChoices):
        NEW = 'NEW', 'New'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'
        FIX = 'FIX', 'Bug Fix'
        OTHER = 'OTHER', 'Other'
    version = models.CharField(max_length=255, default='v1.0.0')
    content = models.TextField(default='Created App v1.0.0')
    type = models.CharField(max_length=255, choices=ChangeType.choices,default=ChangeType.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    app = models.ForeignKey('App', on_delete=models.CASCADE, related_name='changelogs')
    def __str__(self):
        return self.version
    
class AppComment(models.Model):
    class RatingChoice(models.TextChoices):
        ONE = '1', '1'
        ONE_HALF = '1.5', '1.5'
        TWO = '2', '2'
        TWO_HALF = '2.5', '2.5'
        THREE = '3', '3'
        THREE_HALF = '3.5', '3.5'
        FOUR = '4', '4'
        FOUR_HALF = '4.5', '4.5'
        FIVE = '5', '5'
        
    content = models.CharField(max_length=255)
    rating = models.CharField(choices=RatingChoice.choices,default=RatingChoice.FIVE,max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    app = models.ForeignKey('App', on_delete=models.CASCADE)
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='app_comments',null=True)
    def __str__(self):
        return str(self.id)

def app_directory_path(instance, filename): 
    return f'apps/{instance.id}/{filename}'

class App(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to=app_directory_path)
    description = models.CharField(max_length=375)
    tags = models.ManyToManyField(AppTag)
    download_count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    overview = models.TextField()
    config_forms = models.JSONField(null=True,default=list,blank=True, encoder=PrettyJSONEncoder)
    main_file = models.FileField(upload_to=app_directory_path,blank=True,null=True)
    trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('AppCategory', on_delete=models.CASCADE,related_name='apps')
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE, related_name='apps', null=True)
    
    def __str__(self):
        return self.name
