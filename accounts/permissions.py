"""
Central RBAC for news_platform.

Role matrix
-----------
| Action            | normal | admin | super_admin |
|-------------------|--------|-------|-------------|
| Read news         | yes    | yes   | yes         |
| Comment / like    | yes    | yes   | yes         |
| Create news       | no     | yes   | yes         |
| Edit own news     | no     | yes   | yes         |
| Edit any news     | no     | no    | yes         |
| Delete own news   | no     | yes   | yes         |
| Delete any news   | no     | no    | yes         |
| Manage users      | no     | no    | yes         |
| Django admin      | no     | staff | staff+su    |
"""

from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, SAFE_METHODS

ROLE_NORMAL = 'normal'
ROLE_ADMIN = 'admin'
ROLE_SUPER_ADMIN = 'super_admin'


def is_admin(user):
    return user.is_authenticated and user.user_type in (ROLE_ADMIN, ROLE_SUPER_ADMIN)


def is_super_admin(user):
    return user.is_authenticated and user.user_type == ROLE_SUPER_ADMIN


def _role_required(test_func):
    """Require role after @login_required; authenticated failures → 403."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not test_func(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


admin_required = _role_required(is_admin)
super_admin_required = _role_required(is_super_admin)


def can_edit_news(user, news):
    if not user.is_authenticated:
        return False
    if user.user_type == ROLE_SUPER_ADMIN:
        return True
    if user.user_type == ROLE_ADMIN and news.author_id == user.id:
        return True
    return False


def can_delete_news(user, news):
    return can_edit_news(user, news)


def can_manage_user(actor, target):
    """Only super_admin can manage users; cannot demote/delete self."""
    if not is_super_admin(actor):
        return False
    if actor.pk == target.pk:
        return False
    return True


def can_assign_role(actor, new_role):
    """Only super_admin may assign roles."""
    if not is_super_admin(actor):
        return False
    return new_role in (ROLE_NORMAL, ROLE_ADMIN, ROLE_SUPER_ADMIN)


class IsAdminUserType(BasePermission):
    """DRF: admin or super_admin."""

    def has_permission(self, request, view):
        return is_admin(request.user)


class IsSuperAdminUserType(BasePermission):
    """DRF: super_admin only."""

    def has_permission(self, request, view):
        return is_super_admin(request.user)


class IsAuthorOrSuperAdmin(BasePermission):
    """DRF object-level: author (admin) or super_admin."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return can_edit_news(request.user, obj)


class ReadOnlyOrAdmin(BasePermission):
    """Anonymous/authenticated can read; only admins can write."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return is_admin(request.user)
