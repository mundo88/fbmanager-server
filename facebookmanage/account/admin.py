from django.contrib import admin
from .models import Account, AccountSettings  # Import mô hình Account tùy chỉnh
from unfold.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from unfold.decorators import  display
admin.site.unregister(Group)


class AccountSettingsInline(StackedInline):
    model = AccountSettings
    can_delete = False
    verbose_name_plural = 'Settings'
    fk_name = 'user'
    radio_fields = {"theme": admin.VERTICAL}

@admin.register(Account)
class CustomAdminClass(BaseUserAdmin,ModelAdmin): 
    inlines = (AccountSettingsInline,) 
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Thông tin cá nhân"),
            {
                "fields": (("first_name", "last_name"), "email", "avatar"),
                "classes": ["tab"],
            },
        ),
        (
            _("Quyền truy cập"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Ngày quan trọng"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    

    @display(description=_("User"))
    def display_header(self, instance: Account):
        return instance.username

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: Account):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: Account):
        return instance.is_superuser



@admin.register(AccountSettings)
class CustomAdminSettingClass(ModelAdmin):
    radio_fields = {"theme": admin.VERTICAL}

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass