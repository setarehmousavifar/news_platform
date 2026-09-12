"""
Development settings.
"""

from .base import *  # noqa: F403

DEBUG = env.bool('DEBUG', default=True)  # noqa: F405

ALLOWED_HOSTS = env.list(  # noqa: F405
    'ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', '0.0.0.0'],
)

EMAIL_BACKEND = env(  # noqa: F405
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)

# Development-only: allow serving media via Django runserver
SERVE_MEDIA = True

# Latency headers useful while tuning locally
ENABLE_PERF_MIDDLEWARE = env.bool('ENABLE_PERF_MIDDLEWARE', default=True)  # noqa: F405

# Keep CSRF cookies on a single dev hostname (see CanonicalDevHostMiddleware)
CANONICAL_DEV_HOST = env('CANONICAL_DEV_HOST', default='localhost')  # noqa: F405
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

MIDDLEWARE = [
    'news_platform.middleware.CanonicalDevHostMiddleware',
    *MIDDLEWARE,
]
