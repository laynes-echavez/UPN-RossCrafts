"""
URLs para el módulo de auditoría
"""
from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_log_view, name='audit_log'),
    path('export/', views.export_audit_log, name='export_audit_log'),
]
