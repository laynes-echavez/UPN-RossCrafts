"""
Script para resetear la base de datos
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
    
    # Leer el script SQL
    with open('reset_database.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # Ejecutar cada comando GO separadamente
    commands = sql_script.split('GO')
    
    for command in commands:
        command = command.strip()
        if command:
            try:
                cursor.execute(command)
                conn.commit()
            except Exception as e:
                print(f"Error ejecutando comando: {e}")
    
    print("✓ Base de datos limpiada exitosamente")
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {e}")
