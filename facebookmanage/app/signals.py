# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import App,AppChangelog

@receiver(post_save, sender=App)
def create_app_changelog(sender, instance, created, **kwargs):
    if created:
        AppChangelog.objects.create(app=instance)

@receiver(post_save, sender=App)
def save_app_changelog(sender, instance, **kwargs):
    AppChangelog.objects.filter(app=instance).update(app=instance)
