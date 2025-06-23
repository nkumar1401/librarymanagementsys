from django.apps import AppConfig


class LibmanageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libmanage'


def ready(self):
    import libmanage.signals
