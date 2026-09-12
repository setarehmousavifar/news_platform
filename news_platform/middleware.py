"""
Lightweight request timing + DB query count header (DEBUG / ops).
Enable with ENABLE_PERF_MIDDLEWARE=True
"""

import time

from django.conf import settings
from django.db import connection
from django.http import HttpResponseRedirect


class PerformanceStatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(settings, 'ENABLE_PERF_MIDDLEWARE', False):
            return self.get_response(request)

        start = time.perf_counter()
        initial_queries = len(connection.queries)
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        query_count = len(connection.queries) - initial_queries
        response['X-Response-Time-ms'] = f'{elapsed_ms:.1f}'
        response['X-DB-Query-Count'] = str(query_count)
        return response


class CanonicalDevHostMiddleware:
    """
    Redirect local GET requests to one host so CSRF/session cookies stay valid.
    Mixing localhost and 127.0.0.1 breaks Django CSRF on POST.
    """

    _ALIASES = frozenset({'127.0.0.1', '0.0.0.0', '[::1]'})

    def __init__(self, get_response):
        self.get_response = get_response
        self.canonical = getattr(settings, 'CANONICAL_DEV_HOST', 'localhost')

    def __call__(self, request):
        if settings.DEBUG and request.method == 'GET':
            host = request.get_host().split(':')[0]
            if host in self._ALIASES and host != self.canonical:
                port = request.get_port()
                target = self.canonical
                if port not in ('80', '443'):
                    target = f'{self.canonical}:{port}'
                return HttpResponseRedirect(
                    f'{request.scheme}://{target}{request.get_full_path()}'
                )
        return self.get_response(request)
