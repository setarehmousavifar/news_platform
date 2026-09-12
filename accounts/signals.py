from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def sync_django_role_flags(sender, instance, **kwargs):
    """
    Keep Django admin flags aligned with custom user_type roles.
    """
    if instance.user_type == 'super_admin':
        instance.is_staff = True
        instance.is_superuser = True
    elif instance.user_type == 'admin':
        instance.is_staff = True
        instance.is_superuser = False
    else:
        instance.is_staff = False
        instance.is_superuser = False
