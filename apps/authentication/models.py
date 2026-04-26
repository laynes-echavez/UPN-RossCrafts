from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model"""
    ROLE_CHOICES = [
        ('gerente', 'Gerente'),
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='empleado')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rc_users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.username
