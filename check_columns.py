#!/usr/bin/env python
"""
Script para verificar columnas en la tabla facebook_ads_insights
"""
import os
from src.loaders.mysql_loader import MySQLLoader

# Configuración de MySQL desde variables de entorno
config = {
    'host': os.getenv('MYSQL_HOST', 'labsacme.com'),
    'port': int(os.getenv('MYSQL_PORT', 9858)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE', 'metabase')
}

loader = MySQLLoader(config)
loader.connect()

# Obtener columnas
cursor = loader.connection.cursor()
cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM information_schema.COLUMNS 
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'facebook_ads_insights'
    ORDER BY ORDINAL_POSITION
""", (config['database'],))

columns = cursor.fetchall()

print(f"\n{'='*80}")
print(f"COLUMNAS EN facebook_ads_insights ({len(columns)} total)")
print(f"{'='*80}\n")

# Agrupar por tipo
metrics = []
actions = []
costs = []
dates = []
ids = []
others = []

for col_name, data_type in columns:
    if col_name.startswith('action_'):
        actions.append((col_name, data_type))
    elif col_name.startswith('cost_per_'):
        costs.append((col_name, data_type))
    elif 'date' in col_name.lower():
        dates.append((col_name, data_type))
    elif 'id' in col_name.lower() or 'name' in col_name.lower():
        ids.append((col_name, data_type))
    elif col_name in ['spend', 'impressions', 'clicks', 'reach', 'cpc', 'cpm', 'ctr', 'frequency']:
        metrics.append((col_name, data_type))
    else:
        others.append((col_name, data_type))

print("📊 MÉTRICAS BÁSICAS:")
for col, dtype in metrics:
    print(f"  - {col:30s} ({dtype})")

print(f"\n📅 FECHAS:")
for col, dtype in dates:
    print(f"  - {col:30s} ({dtype})")

print(f"\n🆔 IDENTIFICADORES:")
for col, dtype in ids:
    print(f"  - {col:30s} ({dtype})")

print(f"\n✅ ACCIONES ({len(actions)} columnas):")
for col, dtype in actions[:10]:  # Mostrar solo las primeras 10
    print(f"  - {col:50s} ({dtype})")
if len(actions) > 10:
    print(f"  ... y {len(actions) - 10} más")

print(f"\n💰 COSTOS POR ACCIÓN ({len(costs)} columnas):")
for col, dtype in costs[:10]:  # Mostrar solo las primeras 10
    print(f"  - {col:50s} ({dtype})")
if len(costs) > 10:
    print(f"  ... y {len(costs) - 10} más")

print(f"\n📦 OTRAS ({len(others)} columnas):")
for col, dtype in others:
    print(f"  - {col:30s} ({dtype})")

# Verificar si hay datos de leads
cursor.execute("SELECT COUNT(*) FROM facebook_ads_insights WHERE action_lead IS NOT NULL AND action_lead != ''")
lead_count = cursor.fetchone()[0]
print(f"\n🎯 Registros con LEADS: {lead_count}")

cursor.execute("SELECT COUNT(*) FROM facebook_ads_insights WHERE spend > 0")
spend_count = cursor.fetchone()[0]
print(f"💵 Registros con SPEND > 0: {spend_count}")

# Mostrar ejemplo de registro
cursor.execute("""
    SELECT campaign_name, date_start, spend, action_lead, cost_per_lead 
    FROM facebook_ads_insights 
    WHERE spend > 0 
    LIMIT 5
""")
print(f"\n📋 EJEMPLOS DE DATOS:")
print(f"{'Campaign':40s} {'Fecha':12s} {'Spend':>10s} {'Leads':>8s} {'Cost/Lead':>10s}")
print("-" * 85)
for row in cursor.fetchall():
    camp = (row[0] or '')[:38]
    fecha = str(row[1]) if row[1] else ''
    spend = f"${row[2]:,.2f}" if row[2] else ''
    leads = str(row[3]) if row[3] else ''
    cpl = f"${float(row[4]):,.2f}" if row[4] else ''
    print(f"{camp:40s} {fecha:12s} {spend:>10s} {leads:>8s} {cpl:>10s}")

loader.disconnect()
print(f"\n{'='*80}\n")
