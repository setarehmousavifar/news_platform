from django.contrib import admin

from .models import CustomUser, SiteSettings, RoleAuditLog


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'user_type', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'phone_number', 'email')
    ordering = ('-date_joined',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'default_email')
    list_editable = ('default_email',)


@admin.register(RoleAuditLog)
class RoleAuditLogAdmin(admin.ModelAdmin):
    list_display = ('target', 'old_role', 'new_role', 'actor', 'created_at')
    list_filter = ('old_role', 'new_role', 'created_at')
    search_fields = ('target__username', 'actor__username')
    readonly_fields = ('actor', 'target', 'old_role', 'new_role', 'created_at', 'note')
