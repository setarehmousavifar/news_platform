"""
Default to development settings.
Override with DJANGO_SETTINGS_MODULE=news_platform.settings.prod for production.
"""

from .dev import *  # noqa: F403
