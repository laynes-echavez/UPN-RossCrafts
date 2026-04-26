"""
Script de verificación de seguridad y auditoría
Ejecutar: python test_security_audit.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.development')
django.setup()

from django.conf import settings
from apps.audit.models import AuditLog
from apps.authentication.models import User
from datetime import datetime, timedelta


def print_header(title):
    """Imprimir encabezado de sección"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def check_middleware():
    """Verificar que el middleware de auditoría está configurado"""
    print_header("1. VERIFICACIÓN DE MIDDLEWARE")
    
    middleware = settings.MIDDLEWARE
    audit_middleware = 'apps.audit.middleware.AuditMiddleware'
    
    if audit_middleware in middleware:
        print(f"✅ Middleware de auditoría configurado correctamente")
        print(f"   Posición: {middleware.index(audit_middleware) + 1} de {len(middleware)}")
    else:
        print(f"❌ Middleware de auditoría NO encontrado")
        print(f"   Agregar '{audit_middleware}' a MIDDLEWARE en settings")
    
    return audit_middleware in middleware


def check_logging():
    """Verificar configuración de logging"""
    print_header("2. VERIFICACIÓN DE LOGGING")
    
    logging_config = settings.LOGGING
    
    # Verificar handlers
    handlers = logging_config.get('handlers', {})
    required_handlers = ['error_file', 'warning_file', 'activity_file']
    
    print("\nHandlers configurados:")
    for handler in required_handlers:
        if handler in handlers:
            filename = handlers[handler].get('filename', 'N/A')
            print(f"✅ {handler}: {filename}")
        else:
            print(f"❌ {handler}: NO CONFIGURADO")
    
    # Verificar loggers
    loggers = logging_config.get('loggers', {})
    required_loggers = ['apps.sales', 'apps.payments', 'django']
    
    print("\nLoggers configurados:")
    for logger in required_loggers:
        if logger in loggers:
            level = loggers[logger].get('level', 'N/A')
            print(f"✅ {logger}: nivel {level}")
        else:
            print(f"❌ {logger}: NO CONFIGURADO")
    
    # Verificar que existan los directorios de logs
    print("\nDirectorios de logs:")
    logs_dir = settings.BASE_DIR / 'logs'
    if logs_dir.exists():
        print(f"✅ Directorio logs existe: {logs_dir}")
        log_files = ['errors.log', 'warnings.log', 'activity.log', 'django.log']
        for log_file in log_files:
            log_path = logs_dir / log_file
            if log_path.exists():
                size = log_path.stat().st_size
                print(f"   ✅ {log_file}: {size} bytes")
            else:
                print(f"   ⚠️  {log_file}: no existe (se creará al usarse)")
    else:
        print(f"❌ Directorio logs NO existe: {logs_dir}")


def check_security_settings():
    """Verificar configuraciones de seguridad"""
    print_header("3. VERIFICACIÓN DE CONFIGURACIONES DE SEGURIDAD")
    
    security_settings = {
        'SECURE_BROWSER_XSS_FILTER': True,
        'X_FRAME_OPTIONS': 'DENY',
        'SECURE_CONTENT_TYPE_NOSNIFF': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'CSRF_COOKIE_HTTPONLY': True,
    }
    
    print("\nConfiguraciones de seguridad:")
    all_ok = True
    for setting, expected_value in security_settings.items():
        actual_value = getattr(settings, setting, None)
        if actual_value == expected_value:
            print(f"✅ {setting}: {actual_value}")
        else:
            print(f"❌ {setting}: {actual_value} (esperado: {expected_value})")
            all_ok = False
    
    # Verificar configuraciones de producción
    print("\nConfiguraciones de producción (solo en producción):")
    prod_settings = {
        'SECURE_SSL_REDIRECT': False,  # False en desarrollo
        'SESSION_COOKIE_SECURE': False,  # False en desarrollo
        'CSRF_COOKIE_SECURE': False,  # False en desarrollo
    }
    
    for setting, dev_value in prod_settings.items():
        actual_value = getattr(settings, setting, None)
        if settings.DEBUG:
            if actual_value == dev_value:
                print(f"✅ {setting}: {actual_value} (correcto para desarrollo)")
            else:
                print(f"⚠️  {setting}: {actual_value} (debería ser {dev_value} en desarrollo)")
        else:
            if actual_value == True:
                print(f"✅ {setting}: {actual_value} (correcto para producción)")
            else:
                print(f"❌ {setting}: {actual_value} (debería ser True en producción)")
    
    return all_ok


def check_database_security():
    """Verificar seguridad de la base de datos"""
    print_header("4. VERIFICACIÓN DE SEGURIDAD DE BASE DE DATOS")
    
    db_config = settings.DATABASES['default']
    
    print("\nConfiguración de base de datos:")
    print(f"   Engine: {db_config.get('ENGINE')}")
    print(f"   Name: {db_config.get('NAME')}")
    print(f"   Host: {db_config.get('HOST')}")
    
    options = db_config.get('OPTIONS', {})
    print("\nOpciones de seguridad:")
    
    if options.get('Trusted_Connection') == 'yes':
        print(f"✅ Trusted_Connection: yes (Autenticación de Windows)")
    else:
        print(f"⚠️  Trusted_Connection: no configurado")
    
    trust_cert = options.get('TrustServerCertificate', 'no')
    if settings.DEBUG:
        print(f"✅ TrustServerCertificate: {trust_cert} (aceptable en desarrollo)")
    else:
        if trust_cert == 'no':
            print(f"✅ TrustServerCertificate: no (correcto para producción)")
        else:
            print(f"❌ TrustServerCertificate: yes (usar certificado válido en producción)")


def check_audit_logs():
    """Verificar registros de auditoría"""
    print_header("5. VERIFICACIÓN DE REGISTROS DE AUDITORÍA")
    
    try:
        total_logs = AuditLog.objects.count()
        print(f"\n✅ Total de registros de auditoría: {total_logs}")
        
        if total_logs > 0:
            # Últimos 5 registros
            recent_logs = AuditLog.objects.order_by('-timestamp')[:5]
            print("\nÚltimos 5 registros:")
            for log in recent_logs:
                user = log.user.username if log.user else 'Anónimo'
                print(f"   - {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                      f"{user} | {log.action} | {log.url[:50]}")
            
            # Estadísticas por acción
            from django.db.models import Count
            stats = AuditLog.objects.values('action').annotate(count=Count('action')).order_by('-count')
            print("\nEstadísticas por acción:")
            for stat in stats[:10]:
                print(f"   - {stat['action']}: {stat['count']} registros")
        else:
            print("⚠️  No hay registros de auditoría aún")
            print("   Los registros se crearán automáticamente al usar el sistema")
    
    except Exception as e:
        print(f"❌ Error al verificar registros de auditoría: {e}")


def check_stripe_security():
    """Verificar configuración de seguridad de Stripe"""
    print_header("6. VERIFICACIÓN DE SEGURIDAD DE STRIPE")
    
    print("\nClaves de Stripe configuradas:")
    
    if settings.STRIPE_PUBLIC_KEY:
        key_preview = settings.STRIPE_PUBLIC_KEY[:15] + "..."
        print(f"✅ STRIPE_PUBLIC_KEY: {key_preview}")
    else:
        print(f"❌ STRIPE_PUBLIC_KEY: NO CONFIGURADA")
    
    if settings.STRIPE_SECRET_KEY:
        key_preview = settings.STRIPE_SECRET_KEY[:15] + "..."
        print(f"✅ STRIPE_SECRET_KEY: {key_preview}")
    else:
        print(f"❌ STRIPE_SECRET_KEY: NO CONFIGURADA")
    
    if settings.STRIPE_WEBHOOK_SECRET:
        key_preview = settings.STRIPE_WEBHOOK_SECRET[:15] + "..."
        print(f"✅ STRIPE_WEBHOOK_SECRET: {key_preview}")
        print(f"   ⚠️  IMPORTANTE: Verificar firma en webhook es OBLIGATORIO")
    else:
        print(f"❌ STRIPE_WEBHOOK_SECRET: NO CONFIGURADA")
        print(f"   ⚠️  Sin esta clave, los webhooks NO son seguros")


def check_environment_variables():
    """Verificar variables de entorno"""
    print_header("7. VERIFICACIÓN DE VARIABLES DE ENTORNO")
    
    env_file = settings.BASE_DIR / '.env'
    gitignore_file = settings.BASE_DIR / '.gitignore'
    
    print("\nArchivos de configuración:")
    if env_file.exists():
        print(f"✅ Archivo .env existe")
    else:
        print(f"❌ Archivo .env NO existe")
    
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print(f"✅ .env está en .gitignore")
            else:
                print(f"❌ .env NO está en .gitignore (¡CRÍTICO!)")
    else:
        print(f"⚠️  Archivo .gitignore NO existe")
    
    print("\nVariables críticas:")
    critical_vars = {
        'SECRET_KEY': settings.SECRET_KEY,
        'DEBUG': settings.DEBUG,
        'STRIPE_SECRET_KEY': settings.STRIPE_SECRET_KEY,
        'STRIPE_WEBHOOK_SECRET': settings.STRIPE_WEBHOOK_SECRET,
    }
    
    for var_name, var_value in critical_vars.items():
        if var_value:
            if var_name == 'DEBUG':
                print(f"✅ {var_name}: {var_value}")
            else:
                preview = str(var_value)[:10] + "..." if len(str(var_value)) > 10 else str(var_value)
                print(f"✅ {var_name}: {preview}")
        else:
            print(f"❌ {var_name}: NO CONFIGURADA")


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("  VERIFICACIÓN DE SEGURIDAD Y AUDITORÍA - ROSS CRAFTS")
    print("="*60)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Entorno: {'Desarrollo' if settings.DEBUG else 'Producción'}")
    
    # Ejecutar verificaciones
    check_middleware()
    check_logging()
    check_security_settings()
    check_database_security()
    check_audit_logs()
    check_stripe_security()
    check_environment_variables()
    
    # Resumen final
    print_header("RESUMEN")
    print("\n✅ Verificación completada")
    print("\nPróximos pasos:")
    print("1. Revisar cualquier ❌ o ⚠️  en el reporte")
    print("2. Acceder a /dashboard/auditoria/ como gerente")
    print("3. Realizar pruebas de login con rate limiting")
    print("4. Verificar logs en la carpeta logs/")
    print("5. Probar webhook de Stripe con stripe CLI")
    print("\nDocumentación: SEGURIDAD_AUDITORIA_COMPLETADO.md")


if __name__ == '__main__':
    main()
