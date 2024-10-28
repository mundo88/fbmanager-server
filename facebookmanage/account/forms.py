from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm

class UserChangePasswordForm(AdminPasswordChangeForm):
    """
    Form này sẽ dùng để thay đổi mật khẩu trong admin.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
