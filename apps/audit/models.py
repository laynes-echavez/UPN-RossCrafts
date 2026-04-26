from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, 
                            null=True, blank=True)
    action = models.CharField(max_length=10)
    url = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=45)
    status_code = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rc_audit_logs'
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
    
    def __str__(self):
        user_name = self.user.username if self.user else 'Anónimo'
        return f"{user_name} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
