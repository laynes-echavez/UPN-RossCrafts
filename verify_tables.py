"""
Script para verificar las tablas creadas en la base de datos
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
    
    print("=" * 60)
    print("TABLAS CREADAS EN LA BASE DE DATOS")
    print("=" * 60)
    
    # Obtener todas las tablas
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """)
    
    tables = cursor.fetchall()
    
    # Separar tablas por categoría
    rc_tables = []
    django_tables = []
    auth_tables = []
    
    for table in tables:
        table_name = table[0]
        if table_name.startswith('rc_'):
            rc_tables.append(table_name)
        elif table_name.startswith('django_'):
            django_tables.append(table_name)
        elif table_name.startswith('auth_'):
            auth_tables.append(table_name)
    
    print(f"\n📦 TABLAS DE LA APLICACIÓN (Prefijo rc_): {len(rc_tables)}")
    print("-" * 60)
    for table in rc_tables:
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table:<35} ({count} registros)")
    
    print(f"\n🔧 TABLAS DE DJANGO: {len(django_tables)}")
    print("-" * 60)
    for table in django_tables:
        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table:<35} ({count} registros)")
    
    print(f"\n🔐 TABLAS DE AUTENTICACIÓN: {len(auth_tables)}")
    print("-" * 60)
    for table in auth_tables:
        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table:<35} ({count} registros)")
    
    print("\n" + "=" * 60)
    print(f"TOTAL DE TABLAS: {len(tables)}")
    print("=" * 60)
    
    # Verificar estructura de tablas principales
    print("\n📋 ESTRUCTURA DE TABLAS PRINCIPALES:")
    print("=" * 60)
    
    main_tables = ['rc_users', 'rc_products', 'rc_categories', 'rc_customers', 
                   'rc_sales', 'rc_orders', 'rc_suppliers']
    
    for table in main_tables:
        print(f"\n{table}:")
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        for col in columns[:5]:  # Mostrar solo las primeras 5 columnas
            col_name, data_type, max_length, nullable = col
            length_str = f"({max_length})" if max_length else ""
            null_str = "NULL" if nullable == "YES" else "NOT NULL"
            print(f"  - {col_name:<30} {data_type}{length_str:<15} {null_str}")
        
        if len(columns) > 5:
            print(f"  ... y {len(columns) - 5} columnas más")
    
    conn.close()
    print("\n✓ Verificación completada exitosamente")
    
except Exception as e:
    print(f"✗ Error: {e}")
