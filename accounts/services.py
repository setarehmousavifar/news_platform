from django.db import transaction

from .models import RoleAuditLog


def change_user_role(*, actor, target, new_role, note=''):
    """
    Change target.user_type and write an audit log entry.
    Caller must validate permissions first.
    """
    old_role = target.user_type
    if old_role == new_role:
        return target

    with transaction.atomic():
        target.user_type = new_role
        target.save()
        RoleAuditLog.objects.create(
            actor=actor,
            target=target,
            old_role=old_role,
            new_role=new_role,
            note=note,
        )
    return target
