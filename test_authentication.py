"""
Script para probar el sistema de autenticación
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from apps.authentication.models import User
from apps.audit.models import AuditLog

print("=" * 60)
print("PRUEBA DEL SISTEMA DE AUTENTICACIÓN")
print("=" * 60)

# Verificar usuarios
print("\n📋 USUARIOS REGISTRADOS:")
print("-" * 60)
users = User.objects.all()
for user in users:
    print(f"  Usuario: {user.username:<15} | Email: {user.email:<30} | Rol: {user.role}")

# Verificar logs de auditoría
print(f"\n📊 REGISTROS DE AUDITORÍA:")
print("-" * 60)
logs = AuditLog.objects.all().order_by('-timestamp')[:10]
if logs:
    for log in logs:
        user_name = log.user.username if log.user else 'Anónimo'
        print(f"  {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {user_name:<15} | {log.action:<10} | {log.url}")
else:
    print("  No hay registros de auditoría aún")

# Información de prueba
print("\n" + "=" * 60)
print("CREDENCIALES PARA PRUEBAS")
print("=" * 60)
print("\n1. GERENTE:")
print("   Usuario: gerente")
print("   Email: gerente@rosscrafts.com")
print("   Contraseña: Ross2026!")
print("   Dashboard: /reports/")

print("\n2. ADMINISTRADOR:")
print("   Usuario: admin")
print("   Email: admin@rosscrafts.com")
print("   Contraseña: Ross2026!")
print("   Dashboard: /sales/pos/")

print("\n3. EMPLEADO:")
print("   Usuario: empleado")
print("   Email: empleado@rosscrafts.com")
print("   Contraseña: Ross2026!")
print("   Dashboard: /sales/pos/")

print("\n" + "=" * 60)
print("URLS PARA PROBAR")
print("=" * 60)
print("  Login: http://localhost:8000/auth/login/")
print("  Dashboard: http://localhost:8000/auth/dashboard/")
print("  Logout: http://localhost:8000/auth/logout/")
print("  Admin: http://localhost:8000/admin/")

print("\n" + "=" * 60)
print("PRUEBAS SUGERIDAS")
print("=" * 60)
print("1. Login con cada usuario y verificar redirección")
print("2. Intentar acceder a /reports/ como empleado")
print("3. Verificar rate limiting (5 intentos fallidos)")
print("4. Revisar logs de auditoría en admin")
print("5. Probar logout y verificar redirección")

print("\n✓ Sistema listo para pruebas")
print("  Ejecuta: python manage.py runserver")
