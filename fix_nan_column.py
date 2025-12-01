#!/usr/bin/env python3
"""
Script para eliminar la columna 'nan' de la tabla facebook_ads_insights
Ejecutar una vez para limpiar el esquema corrupto
"""
import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.docker')

def fix_nan_column():
    """Elimina la columna 'nan' si existe"""
    config = {
        'host': os.getenv('MYSQL_HOST', 'mysql'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE')
    }
    
    print(f"🔍 Conectando a {config['host']}:{config['port']}")
    print(f"   Database: {config['database']}")
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = 'facebook_ads_insights'
        """, (config['database'],))
        
        if cursor.fetchone()[0] == 0:
            print("ℹ️  La tabla facebook_ads_insights no existe todavía")
            cursor.close()
            conn.close()
            return
        
        # Obtener todas las columnas
        cursor.execute("SHOW COLUMNS FROM facebook_ads_insights")
        columns = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📋 Columnas actuales ({len(columns)}):")
        for col in columns:
            print(f"   - {col}")
        
        # Buscar columnas con nombres inválidos
        invalid_names = ['nan', 'none', 'nat', 'null', 'undefined']
        columns_to_drop = [col for col in columns if col.lower() in invalid_names]
        
        if not columns_to_drop:
            print("\n✅ No hay columnas inválidas. Todo está bien!")
            cursor.close()
            conn.close()
            return
        
        # Eliminar columnas inválidas
        print(f"\n🔧 Eliminando {len(columns_to_drop)} columna(s) inválida(s)...")
        for col in columns_to_drop:
            print(f"   Eliminando: {col}")
            try:
                cursor.execute(f"ALTER TABLE facebook_ads_insights DROP COLUMN `{col}`")
                conn.commit()
                print(f"   ✅ Eliminada: {col}")
            except Exception as e:
                print(f"   ❌ Error eliminando {col}: {e}")
        
        print("\n✅ Limpieza completada!")
        
        # Mostrar columnas finales
        cursor.execute("SHOW COLUMNS FROM facebook_ads_insights")
        final_columns = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Columnas finales ({len(final_columns)}):")
        for col in final_columns:
            print(f"   - {col}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    fix_nan_column()
