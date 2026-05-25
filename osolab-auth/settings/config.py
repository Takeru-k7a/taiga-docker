# -*- coding: utf-8 -*-
import os

from kombu import Queue

from .common import *  # noqa: F401,F403

DEBUG = False

SECRET_KEY = os.getenv("TAIGA_SECRET_KEY", "change-me")
TAIGA_SITES_SCHEME = os.getenv("TAIGA_SITES_SCHEME", "http")
TAIGA_SITES_DOMAIN = os.getenv("TAIGA_SITES_DOMAIN", "localhost:9000")
FORCE_SCRIPT_NAME = os.getenv("TAIGA_SUBPATH", "")
TAIGA_URL = f"{TAIGA_SITES_SCHEME}://{TAIGA_SITES_DOMAIN}{FORCE_SCRIPT_NAME}"

SITES = {
    "api": {
        "name": "api",
        "scheme": TAIGA_SITES_SCHEME,
        "domain": TAIGA_SITES_DOMAIN,
    },
    "front": {
        "name": "front",
        "scheme": TAIGA_SITES_SCHEME,
        "domain": f"{TAIGA_SITES_DOMAIN}{FORCE_SCRIPT_NAME}",
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "taiga"),
        "USER": os.getenv("POSTGRES_USER", "taiga"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "taiga"),
        "HOST": os.getenv("POSTGRES_HOST", "taiga-db"),
        "PORT": os.getenv("POSTGRES_PORT", ""),
    }
}

MEDIA_URL = f"{TAIGA_URL}/media/"
STATIC_URL = f"{TAIGA_URL}/static/"
DEFAULT_FILE_STORAGE = "taiga_contrib_protected.storage.ProtectedFileSystemStorage"
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "changeme@example.com")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.host.example.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

RABBITMQ_USER = os.getenv("RABBITMQ_USER", "taiga")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "taiga")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "taiga")

EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
EVENTS_PUSH_BACKEND_OPTIONS = {
    "url": f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@taiga-events-rabbitmq:5672/{RABBITMQ_VHOST}",
}

CELERY_ENABLED = os.getenv("CELERY_ENABLED", "True") == "True"
CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@taiga-async-rabbitmq:5672/{RABBITMQ_VHOST}"
)
CELERY_RESULT_BACKEND = None
CELERY_ACCEPT_CONTENT = ["pickle"]
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Tokyo")
CELERY_TASK_DEFAULT_QUEUE = "tasks"
CELERY_QUEUES = (
    Queue("tasks", routing_key="task.#"),
    Queue("transient", routing_key="transient.#", delivery_mode=1),
)
CELERY_TASK_DEFAULT_EXCHANGE = "tasks"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "topic"
CELERY_TASK_DEFAULT_ROUTING_KEY = "task.default"

ENABLE_TELEMETRY = os.getenv("ENABLE_TELEMETRY", "False") == "True"
PUBLIC_REGISTER_ENABLED = False

INSTALLED_APPS += [
    "mozilla_django_oidc",
    "taiga_contrib_oidc_auth",
]

AUTHENTICATION_BACKENDS = list(AUTHENTICATION_BACKENDS) + [
    "taiga_contrib_oidc_auth.oidc.TaigaOIDCAuthenticationBackend",
]

ROOT_URLCONF = "settings.urls"

OIDC_CALLBACK_CLASS = (
    "taiga_contrib_oidc_auth.views.TaigaOIDCAuthenticationCallbackView"
)
OIDC_RP_SCOPES = os.getenv("OIDC_RP_SCOPES", "openid profile email")
OIDC_RP_SIGN_ALGO = os.getenv("OIDC_RP_SIGN_ALGO", "RS256")
OIDC_BASE_URL = os.getenv("OIDC_BASE_URL", "http://localhost:5040")
OIDC_OP_JWKS_ENDPOINT = os.getenv(
    "OIDC_OP_JWKS_ENDPOINT", f"{OIDC_BASE_URL}/.well-known/jwks.json"
)
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv(
    "OIDC_OP_AUTHORIZATION_ENDPOINT", f"{OIDC_BASE_URL}/connect/authorize"
)
OIDC_OP_TOKEN_ENDPOINT = os.getenv(
    "OIDC_OP_TOKEN_ENDPOINT", f"{OIDC_BASE_URL}/connect/token"
)
OIDC_OP_USER_ENDPOINT = os.getenv(
    "OIDC_OP_USER_ENDPOINT", f"{OIDC_BASE_URL}/connect/userinfo"
)
OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET")
