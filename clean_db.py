"""
Script para limpiar completamente la base de datos
"""
import pyodbc

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ARJAY-LAYNES\\SQLEXPRESS01;'
        'DATABASE=ross_crafts_db;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    
    cursor = conn.cursor()
    
    print("Desactivando restricciones de clave foránea...")
    
    # Obtener todas las tablas
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    # Desactivar todas las restricciones
    for table in tables:
        try:
            cursor.execute(f"ALTER TABLE [{table}] NOCHECK CONSTRAINT ALL")
            conn.commit()
        except:
            pass
    
    print(f"Eliminando {len(tables)} tablas...")
    
    # Eliminar todas las tablas
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE [{table}]")
            conn.commit()
            print(f"  ✓ Eliminada: {table}")
        except Exception as e:
            print(f"  ✗ Error eliminando {table}: {e}")
    
    print("\n✓ Base de datos limpiada exitosamente")
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
