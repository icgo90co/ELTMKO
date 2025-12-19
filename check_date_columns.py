"""
Quick script to check which tables have date columns
"""
import os
import yaml
from src.loaders.mysql_loader import MySQLLoader

# Load config
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Get MySQL config
mysql_config = None
for dest in config.get('destinations', []):
    if dest.get('type') == 'mysql':
        mysql_config = dest.get('config', {})
        break

if not mysql_config:
    print("❌ No MySQL destination configured")
    exit(1)

# Connect to MySQL
loader = MySQLLoader(mysql_config)
loader.connect()

cursor = loader.connection.cursor()

# Get all facebook_ads tables
cursor.execute("SHOW TABLES LIKE 'facebook_ads_%'")
tables = cursor.fetchall()

print("\n" + "="*60)
print("📊 VERIFICACIÓN DE COLUMNAS DE FECHA EN TABLAS")
print("="*60 + "\n")

for (table_name,) in tables:
    # Check for date_start column
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'date_start'")
    has_date_start = cursor.fetchone() is not None
    
    # Check for date_stop column
    cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'date_stop'")
    has_date_stop = cursor.fetchone() is not None
    
    # Count rows
    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
    row_count = cursor.fetchone()[0]
    
    status = "✅" if has_date_start and has_date_stop else "❌"
    date_cols = "Sí" if has_date_start and has_date_stop else "No"
    
    print(f"{status} {table_name}")
    print(f"   - Columnas de fecha: {date_cols}")
    print(f"   - Registros: {row_count:,}")
    
    if has_date_start:
        # Get date range if available
        try:
            cursor.execute(f"SELECT MIN(date_start), MAX(date_start) FROM `{table_name}`")
            result = cursor.fetchone()
            if result[0]:
                print(f"   - Rango: {result[0]} a {result[1]}")
        except:
            pass
    
    print()

cursor.close()
loader.disconnect()

print("="*60)
print("\n💡 Tip: Solo las tablas con ✅ pueden usar filtros de fecha")
print("   Las demás tablas pueden usar filtros personalizados por otros campos\n")
