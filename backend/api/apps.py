from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # 匯入 signal handler，確保被註冊
        import api.signals  # noqa: F401
