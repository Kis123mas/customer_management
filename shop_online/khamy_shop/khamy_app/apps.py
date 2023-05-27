from django.apps import AppConfig


class KhamyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'khamy_app'

    def ready(self):
        import khamy_app.signals
