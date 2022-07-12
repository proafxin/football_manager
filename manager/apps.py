"""Configure app"""

from django.apps import AppConfig


class ManagerConfig(AppConfig):
    """Configuration class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "manager"

    def ready(self) -> None:
        import manager.signals

        return super().ready()
