from django.apps import AppConfig


class FacebookAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'facebook_account'
    def ready(self):
        import facebook_account.signals