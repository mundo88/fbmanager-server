# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChromeProfile, FacebookAccount

@receiver(post_save, sender=FacebookAccount)
def create_chrome_profile(sender, instance, created, **kwargs):
    if created:
        ChromeProfile.objects.create(fbaccount=instance)

@receiver(post_save, sender=FacebookAccount)
def save_chrome_profile(sender, instance, **kwargs):
    ChromeProfile.objects.filter(fbaccount=instance).update(fbaccount=instance)
