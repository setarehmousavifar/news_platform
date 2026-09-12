from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /accounts/dashboard/',
        'Disallow: /accounts/manage_users/',
        'Disallow: /news/manage/',
        'Disallow: /news/create/',
        'Disallow: /api/',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')
