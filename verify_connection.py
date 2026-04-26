"""
Script para verificar la conexión a SQL Server
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
    print("✓ Conexión exitosa a SQL Server")
    print(f"✓ Conexión: {conn}")
    
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print(f"✓ Versión de SQL Server: {row[0][:50]}...")
    
    conn.close()
    print("✓ Conexión cerrada correctamente")
    
except pyodbc.Error as e:
    print("✗ Error al conectar a SQL Server:")
    print(f"  {e}")
