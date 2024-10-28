from django.contrib import admin
from app_task.models import AppTask
from unfold.admin import ModelAdmin

@admin.register(AppTask)
class CustomAdminClass(ModelAdmin):
    pass