from django.apps import AppConfig


class CeleryShowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_show'


    def ready(self):
        import celery_show.signals
