from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES["default"]["NAME"] = "docuparse"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS (allow frontend locally)
CORS_ALLOW_ALL_ORIGINS = True

# DRF Debug
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework.permissions.AllowAny"
]

# Celery (run synchronously for debugging)
CELERY_TASK_ALWAYS_EAGER = True