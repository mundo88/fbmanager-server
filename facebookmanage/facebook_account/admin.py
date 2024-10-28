from django.contrib import admin
from .models import FacebookAccount, ChromeProfile
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm
from import_export.admin import ImportExportModelAdmin
from unfold.decorators import action, display
from django.utils.translation import gettext_lazy as _
from account.models import Account
# Inline cho ChromeProfile
class AccountSettingsInline(StackedInline):
    model = ChromeProfile
    can_delete = True
    verbose_name_plural = 'Chrome Profile'


# Đăng ký model FacebookAccount với admin
@admin.register(FacebookAccount)
class CustomAdminClass(ImportExportModelAdmin, ModelAdmin):
    inlines = [AccountSettingsInline]
    import_form_class = ImportForm  # Sử dụng form tùy chỉnh
    export_form_class = SelectableFieldsExportForm
    list_display = [
        "uid",
        'password',
        '_2fa',
        'cookie',
    ]
    autocomplete_fields = [
        "collaborators",
    ]
    fieldsets = (
        (
            _('Thông tin bảo mật'),
            {
                "fields": (
                    ("uid","password"),
                    '_2fa',
                    'access_token',
                    "cookie",
                    "collaborators",
                    'active'
                ),
                "classes": ["tab"],
            },
        ),
         (
            _('Thông tin tài khoản'),
            {
                "fields": (
                    'name',
                    ("email","pass_mail"),
                    "phone_number",
                    "profile_picture",
                    ('created_at', 'updated_at'),
                    'last_login'
                ),
                "classes": ["tab"],
            },
        ),
    )
    readonly_fields = [
        "created_at",
        "updated_at",
        "last_login",
    ]