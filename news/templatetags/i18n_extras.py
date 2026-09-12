from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def url_for_language(context, lang_code):
    """Return the current path translated for the given language code."""
    request = context.get('request')
    if not request:
        return '/'
    return translate_url(request.get_full_path(), lang_code)
