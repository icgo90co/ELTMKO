"""
Script de ejemplo para usar el sistema ELT programáticamente
"""
from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator
from src.extractors import FacebookAdsExtractor
from src.loaders import MySQLLoader
import pandas as pd


def ejemplo_basico():
    """Ejemplo básico de uso del sistema"""
    print("🔄 Ejemplo: Ejecución básica de pipeline\n")
    
    # Cargar configuración
    config_manager = ConfigManager('config/config.yaml')
    setup_logger(config_manager.get_logging_config())
    
    # Crear y ejecutar orquestador
    orchestrator = Orchestrator(config_manager)
    results = orchestrator.run_all()
    
    print(f"\n✅ Resultados: {results}")


def ejemplo_extraccion_personalizada():
    """Ejemplo de extracción personalizada de Facebook Ads"""
    print("📊 Ejemplo: Extracción personalizada de Facebook Ads\n")
    
    # Configuración manual
    fb_config = {
        'app_id': 'tu_app_id',
        'app_secret': 'tu_app_secret',
        'access_token': 'tu_token',
        'ad_account_id': 'act_tu_account'
    }
    
    # Crear extractor
    extractor = FacebookAdsExtractor(fb_config)
    
    # Extraer campañas
    campaigns_df = extractor.extract_campaigns()
    print(f"Campañas extraídas: {len(campaigns_df)}")
    print(campaigns_df.head())
    
    # Extraer insights de los últimos 7 días
    insights_df = extractor.extract_insights(
        level='campaign',
        date_range=7
    )
    print(f"\nInsights extraídos: {len(insights_df)}")
    print(insights_df.head())


def ejemplo_carga_mysql():
    """Ejemplo de carga de datos a MySQL"""
    print("💾 Ejemplo: Carga de datos a MySQL\n")
    
    # Configuración MySQL
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'elt_data'
    }
    
    # Crear datos de ejemplo
    data = {
        'id': [1, 2, 3],
        'name': ['Campaña A', 'Campaña B', 'Campaña C'],
        'status': ['ACTIVE', 'PAUSED', 'ACTIVE'],
        'spend': [100.50, 250.75, 175.25]
    }
    df = pd.DataFrame(data)
    
    # Cargar a MySQL
    loader = MySQLLoader(mysql_config)
    
    with loader:
        # Upsert con clave única en 'id'
        loader.upsert_dataframe(
            df=df,
            table_name='ejemplo_campañas',
            key_columns=['id']
        )
    
    print("✅ Datos cargados exitosamente")


def ejemplo_pipeline_completo():
    """Ejemplo de pipeline completo personalizado"""
    print("🔄 Ejemplo: Pipeline completo personalizado\n")
    
    # Configuración
    fb_config = {
        'app_id': 'tu_app_id',
        'app_secret': 'tu_app_secret',
        'access_token': 'tu_token',
        'ad_account_id': 'act_tu_account'
    }
    
    mysql_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'elt_data'
    }
    
    # Extracción
    extractor = FacebookAdsExtractor(fb_config)
    campaigns_df = extractor.extract_campaigns()
    
    # Transformación (ejemplo simple)
    campaigns_df['nombre_mayusculas'] = campaigns_df['name'].str.upper()
    campaigns_df['fecha_proceso'] = pd.Timestamp.now()
    
    # Carga
    loader = MySQLLoader(mysql_config)
    with loader:
        loader.upsert_dataframe(
            df=campaigns_df,
            table_name='fb_campaigns_procesadas',
            key_columns=['id']
        )
    
    print(f"✅ Pipeline completado: {len(campaigns_df)} registros procesados")


if __name__ == '__main__':
    print("=" * 60)
    print("Ejemplos de Uso del Sistema ELT")
    print("=" * 60)
    print()
    
    # Descomentar el ejemplo que quieras ejecutar:
    
    # ejemplo_basico()
    # ejemplo_extraccion_personalizada()
    # ejemplo_carga_mysql()
    # ejemplo_pipeline_completo()
    
    print("\n💡 Consejo: Edita este archivo y descomenta el ejemplo que quieras ejecutar")
