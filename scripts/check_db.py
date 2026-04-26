"""
Script para verificar conexión a SQL Server antes del despliegue.

Uso: python scripts/check_db.py
"""
import pyodbc
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

def check_database_connection():
    """Verificar conexión a SQL Server"""
    print("=" * 60)
    print("VERIFICACIÓN DE CONEXIÓN A SQL SERVER")
    print("=" * 60)
    print()
    
    # Obtener configuración
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    
    if not db_host or not db_name:
        print("❌ ERROR: Variables DB_HOST y DB_NAME no están configuradas en .env")
        return False
    
    print(f"Host: {db_host}")
    print(f"Base de datos: {db_name}")
    print()
    
    try:
        # Construir cadena de conexión
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_host};"
            f"DATABASE={db_name};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
        
        print("Intentando conectar...")
        conn = pyodbc.connect(conn_str, timeout=10)
        
        print("✅ Conexión a SQL Server exitosa")
        print()
        
        # Obtener información del servidor
        cursor = conn.cursor()
        
        # Versión de SQL Server
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Versión SQL Server:")
        print(f"   {version[:100]}...")
        print()
        
        # Nombre de la base de datos
        cursor.execute("SELECT DB_NAME()")
        current_db = cursor.fetchone()[0]
        print(f"Base de datos actual: {current_db}")
        print()
        
        # Usuario actual
        cursor.execute("SELECT SYSTEM_USER, USER_NAME()")
        system_user, user_name = cursor.fetchone()
        print(f"Usuario del sistema: {system_user}")
        print(f"Usuario de BD: {user_name}")
        print()
        
        # Verificar permisos
        cursor.execute("""
            SELECT 
                dp.name AS role_name
            FROM sys.database_role_members drm
            JOIN sys.database_principals dp ON drm.role_principal_id = dp.principal_id
            JOIN sys.database_principals dp2 ON drm.member_principal_id = dp2.principal_id
            WHERE dp2.name = USER_NAME()
        """)
        
        roles = cursor.fetchall()
        if roles:
            print("Roles asignados:")
            for role in roles:
                print(f"   - {role[0]}")
        else:
            print("⚠️  ADVERTENCIA: No se encontraron roles asignados")
        
        print()
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]
        print(f"Tablas en la base de datos: {table_count}")
        
        if table_count == 0:
            print("⚠️  La base de datos está vacía. Ejecutar migraciones.")
        
        conn.close()
        
        print()
        print("=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        
        return True
        
    except pyodbc.Error as e:
        print()
        print("=" * 60)
        print("❌ ERROR DE CONEXIÓN")
        print("=" * 60)
        print()
        print(f"Detalles del error:")
        print(f"   {str(e)}")
        print()
        print("Posibles soluciones:")
        print("   1. Verificar que SQL Server Express está ejecutándose")
        print("   2. Verificar el nombre del servidor en .env (DB_HOST)")
        print("   3. Verificar que la base de datos existe")
        print("   4. Verificar permisos del usuario de Windows")
        print("   5. Verificar que ODBC Driver 17 está instalado")
        print()
        
        return False
    
    except Exception as e:
        print()
        print(f"❌ Error inesperado: {str(e)}")
        return False


if __name__ == '__main__':
    success = check_database_connection()
    sys.exit(0 if success else 1)
