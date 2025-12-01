#!/usr/bin/env python3
"""
Script de prueba para replicar el error 'Unknown column nan in SELECT'
"""
import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv('.env.docker')

def test_insert():
    """Prueba INSERT con datos de ejemplo"""
    config = {
        'host': os.getenv('MYSQL_HOST'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'database': os.getenv('MYSQL_DATABASE')
    }
    
    print("🔍 Probando INSERT en facebook_ads_insights...")
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Crear DataFrame de prueba
        test_data = {
            'date_start': ['2025-12-01'],
            'date_stop': ['2025-12-01'],
            'campaign_id': ['123'],
            'campaign_name': ['Test'],
            'impressions': [100],
            'clicks': [10],
            'spend': [50],
            'reach': [80],
            'ctr': [0.1],
            'cpc': [5.0],
            'cpm': [62.5],
            'frequency': [1.25],
            'actions': ['{}'],
            'video_play_actions': ['{}'],
            'inline_link_clicks': ['5']
        }
        
        df = pd.DataFrame(test_data)
        
        print(f"📊 DataFrame columns: {list(df.columns)}")
        print(f"   Shape: {df.shape}")
        
        # Preparar INSERT
        columns = list(df.columns)
        columns_str = ", ".join([f"`{col}`" for col in columns])
        placeholders = ", ".join(["%s"] * len(columns))
        
        insert_query = f"INSERT INTO facebook_ads_insights ({columns_str}) VALUES ({placeholders})"
        
        print(f"\n📝 Query: {insert_query[:100]}...")
        
        # Ejecutar INSERT
        data = [tuple(row) for row in df.values]
        cursor.executemany(insert_query, data)
        conn.commit()
        
        print(f"\n✅ INSERT exitoso! {cursor.rowcount} fila(s) insertada(s)")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_insert()
