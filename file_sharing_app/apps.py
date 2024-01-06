from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'
    verbose_name = 'Your App Name'

    def ready(self):
        import file_sharing_app.api_token_auth

class FileSharingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_sharing_app'
