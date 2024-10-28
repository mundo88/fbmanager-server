# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, AccountSettings

@receiver(post_save, sender=Account)
def create_account_settings(sender, instance, created, **kwargs):
    if created:
        AccountSettings.objects.create(user=instance)

@receiver(post_save, sender=Account)
def save_account_settings(sender, instance, **kwargs):
    instance.settings.save()
