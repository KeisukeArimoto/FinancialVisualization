from django.apps import AppConfig


class SaveSecurityReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saveSecurityReports'

    def ready(self):
        from .ap_scheduler import start
        start()
