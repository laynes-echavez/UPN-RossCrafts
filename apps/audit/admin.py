from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'url', 'ip_address', 'status_code', 'timestamp']
    list_filter = ['action', 'status_code', 'timestamp']
    search_fields = ['user__username', 'url', 'ip_address']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
