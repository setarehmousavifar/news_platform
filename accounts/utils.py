from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme


def get_safe_redirect_url(request, next_url, default='home'):
    """
    Return a safe redirect target, blocking open-redirect attacks.
    """
    if not next_url:
        return redirect(default)

    if url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect(default)
