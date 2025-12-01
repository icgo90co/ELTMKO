#!/usr/bin/env python3
"""Script para verificar la configuración en MySQL"""
import os
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno
load_dotenv('.env.docker')

# Conectar a MySQL
config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

print(f"🔍 Conectando a MySQL: {config['host']}:{config['port']}")
print(f"   Base de datos: {config['database']}")
print(f"   Usuario: {config['user']}")
print()

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    # Verificar tabla config_sources
    cursor.execute("SHOW TABLES LIKE 'config_sources'")
    if cursor.fetchone():
        print("✅ Tabla 'config_sources' existe")
        
        # Verificar configuración de Facebook
        cursor.execute("SELECT source_name, is_active, config FROM config_sources WHERE source_name = 'facebook_ads'")
        row = cursor.fetchone()
        
        if row:
            print(f"✅ Configuración de Facebook Ads encontrada:")
            print(f"   Estado: {'Activo' if row[1] else 'Inactivo'}")
            print(f"   Config: {row[2][:100]}..." if len(row[2]) > 100 else f"   Config: {row[2]}")
        else:
            print("❌ No hay configuración de Facebook Ads")
            print("   El modal aparecerá porque no hay config guardada")
    else:
        print("❌ Tabla 'config_sources' NO existe")
        print("   Necesitas ejecutar init-db.sql primero")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
