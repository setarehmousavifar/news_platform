"""
Production settings.
"""

from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')  # noqa: F405

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])  # noqa: F405

SERVE_MEDIA = False
ENABLE_PERF_MIDDLEWARE = env.bool('ENABLE_PERF_MIDDLEWARE', default=False)  # noqa: F405

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30

TEMPLATES[0]['OPTIONS']['context_processors'] = [  # noqa: F405
    cp for cp in TEMPLATES[0]['OPTIONS']['context_processors']  # noqa: F405
    if cp != 'django.template.context_processors.debug'
]

# Hide OpenAPI UI in production unless explicitly enabled
if not env.bool('ENABLE_API_DOCS', default=False):  # noqa: F405
    SPECTACULAR_SETTINGS = {  # noqa: F405
        **SPECTACULAR_SETTINGS,  # noqa: F405
        'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
    }

LOGGING['handlers']['file']['filename'] = BASE_DIR / 'logs' / 'django.log'  # noqa: F405
LOGGING['root']['handlers'] = ['console', 'file']  # noqa: F405
LOGGING['loggers']['django']['handlers'] = ['console', 'file']  # noqa: F405
