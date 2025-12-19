"""
Web API for ELT System Configuration
Provides REST endpoints to manage sources, destinations, and pipelines
"""
import logging
import json
import threading
from flask import Flask, jsonify, request, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from datetime import datetime
import os
import yaml

from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
CORS(app)

# Global variables
config_manager = None
orchestrator = None

# Progress tracking
progress_store = {}
progress_lock = threading.Lock()


def init_app(config_path: str = "config/config.yaml"):
    """Initialize the application"""
    global config_manager, orchestrator
    
    config_manager = ConfigManager(config_path)
    setup_logger(config_manager.get_logging_config())
    orchestrator = Orchestrator(config_manager)
    
    # Initialize Facebook Ads configuration from environment variables
    _init_facebook_config_from_env()
    
    logger.info("Web API initialized")


def _init_facebook_config_from_env():
    """Initialize Facebook Ads configuration from environment variables if not exists"""
    try:
        from src.loaders.mysql_loader import MySQLLoader
        
        # Get credentials from environment
        app_id = os.getenv('FACEBOOK_APP_ID')
        app_secret = os.getenv('FACEBOOK_APP_SECRET')
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        ad_account_id = os.getenv('FACEBOOK_AD_ACCOUNT_ID')
        
        # Only proceed if all credentials are set
        if not all([app_id, app_secret, access_token, ad_account_id]):
            logger.info("Facebook credentials not fully configured in environment variables")
            return
        
        # Connect to MySQL
        mysql_config = config_manager.get_destination_config('mysql_main')
        loader = MySQLLoader(mysql_config)
        loader.ensure_connection()
        
        cursor = loader.connection.cursor()
        
        # Check if facebook_ads source already exists
        cursor.execute("SELECT COUNT(*) FROM config_sources WHERE source_name = 'facebook_ads'")
        exists = cursor.fetchone()[0] > 0
        
        if not exists:
            logger.info("Initializing Facebook Ads configuration from environment variables...")
            
            # Insert Facebook Ads configuration
            cursor.execute("""
                INSERT INTO config_sources (source_name, source_type, config, is_active)
                VALUES ('facebook_ads', 'facebook_ads', %s, 1)
            """, (yaml.dump({
                'app_id': app_id,
                'app_secret': app_secret,
                'access_token': access_token,
                'ad_account_id': ad_account_id
            }),))
            
            loader.connection.commit()
            logger.info("✅ Facebook Ads configuration initialized successfully")
        else:
            logger.info("Facebook Ads configuration already exists in database")
        
        cursor.close()
        loader.close()
        
    except Exception as e:
        logger.warning(f"Could not initialize Facebook configuration from environment: {e}")


# Serve static files
@app.route('/')
def index():
    """Serve the web interface"""
    return send_from_directory('static', 'index.html')


# Health check
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


# Sources endpoints
@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get all sources"""
    try:
        sources = config_manager.get_sources()
        return jsonify({
            'success': True,
            'data': sources
        })
    except Exception as e:
        logger.error(f"Error getting sources: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sources/<source_name>', methods=['GET'])
def get_source(source_name):
    """Get specific source by name"""
    try:
        source = config_manager.get_source(source_name)
        return jsonify({
            'success': True,
            'data': source
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        logger.error(f"Error getting source: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Destinations endpoints
@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get all destinations"""
    try:
        destinations = config_manager.get_destinations()
        return jsonify({
            'success': True,
            'data': destinations
        })
    except Exception as e:
        logger.error(f"Error getting destinations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/destinations/<destination_name>', methods=['GET'])
def get_destination(destination_name):
    """Get specific destination by name"""
    try:
        destination = config_manager.get_destination(destination_name)
        return jsonify({
            'success': True,
            'data': destination
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        logger.error(f"Error getting destination: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Pipeline endpoints
@app.route('/api/pipelines', methods=['GET'])
def get_pipelines():
    """Get all configured pipelines"""
    try:
        pipelines = []
        for pipeline in orchestrator.pipelines:
            pipelines.append({
                'source': pipeline.source_name,
                'source_type': pipeline.source_type,
                'destination': pipeline.destination_name
            })
        
        return jsonify({
            'success': True,
            'data': pipelines
        })
    except Exception as e:
        logger.error(f"Error getting pipelines: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/pipelines/run', methods=['POST'])
def run_pipelines():
    """Run all pipelines"""
    try:
        logger.info("API request: Running all pipelines")
        results = orchestrator.run_all()
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        logger.error(f"Error running pipelines: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/pipelines/run/<source_name>', methods=['POST'])
def run_pipeline(source_name):
    """Run specific pipeline by source name"""
    try:
        logger.info(f"API request: Running pipeline for source '{source_name}'")
        result = orchestrator.run_source(source_name)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/pipelines/run/<source_name>/stream', methods=['GET'])
def run_pipeline_stream(source_name):
    """Run pipeline with real-time progress updates using Server-Sent Events"""
    import queue
    import threading
    
    # Cola para comunicación entre threads
    progress_queue = queue.Queue()
    
    def progress_callback(message, progress=None):
        """Callback para enviar progreso"""
        progress_queue.put({
            'message': message,
            'progress': progress
        })
    
    def run_with_progress():
        """Ejecuta el pipeline y envía progreso"""
        try:
            logger.info(f"API request: Running pipeline with progress for source '{source_name}'")
            
            # Modificar temporalmente el orchestrator para usar el callback
            result = orchestrator.run_source_with_progress(source_name, progress_callback)
            
            progress_queue.put({
                'done': True,
                'success': True,
                'result': result
            })
        except Exception as e:
            logger.error(f"Error running pipeline: {e}")
            progress_queue.put({
                'done': True,
                'success': False,
                'error': str(e)
            })
    
    def generate():
        """Genera eventos SSE"""
        # Iniciar pipeline en thread separado
        thread = threading.Thread(target=run_with_progress)
        thread.daemon = True
        thread.start()
        
        # Enviar eventos de progreso
        while True:
            try:
                event = progress_queue.get(timeout=30)
                
                if event.get('done'):
                    if event.get('success'):
                        yield f"data: {json.dumps({'type': 'complete', 'result': event.get('result')})}\n\n"
                    else:
                        yield f"data: {json.dumps({'type': 'error', 'error': event.get('error')})}\n\n"
                    break
                else:
                    yield f"data: {json.dumps({'type': 'progress', 'message': event.get('message'), 'progress': event.get('progress')})}\n\n"
            except queue.Empty:
                # Timeout - enviar keepalive
                yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
        
        thread.join(timeout=1)
    
    response = Response(stream_with_context(generate()), mimetype='text/event-stream')
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['X-Accel-Buffering'] = 'no'
    return response


@app.route('/api/config/reload', methods=['POST'])
def reload_config():
    """Reload configuration from file"""
    try:
        global orchestrator
        
        config_manager.reload()
        orchestrator = Orchestrator(config_manager)
        
        logger.info("Configuration reloaded via API")
        
        return jsonify({
            'success': True,
            'message': 'Configuration reloaded successfully'
        })
    except Exception as e:
        logger.error(f"Error reloading configuration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sources/<source_name>/config', methods=['POST'])
def update_source_config(source_name):
    """Update source configuration"""
    try:
        data = request.get_json()
        logger.info(f"API request: Updating config for source '{source_name}'")
        
        # Update environment variables
        import os
        if 'app_id' in data:
            os.environ['FACEBOOK_APP_ID'] = data['app_id']
        if 'app_secret' in data:
            os.environ['FACEBOOK_APP_SECRET'] = data['app_secret']
        if 'access_token' in data:
            os.environ['FACEBOOK_ACCESS_TOKEN'] = data['access_token']
        if 'ad_account_id' in data:
            os.environ['FACEBOOK_AD_ACCOUNT_ID'] = data['ad_account_id']
        
        # Update .env file
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('FACEBOOK_APP_ID='):
                        f.write(f"FACEBOOK_APP_ID={data.get('app_id', '')}\n")
                    elif line.startswith('FACEBOOK_APP_SECRET='):
                        f.write(f"FACEBOOK_APP_SECRET={data.get('app_secret', '')}\n")
                    elif line.startswith('FACEBOOK_ACCESS_TOKEN='):
                        f.write(f"FACEBOOK_ACCESS_TOKEN={data.get('access_token', '')}\n")
                    elif line.startswith('FACEBOOK_AD_ACCOUNT_ID='):
                        f.write(f"FACEBOOK_AD_ACCOUNT_ID={data.get('ad_account_id', '')}\n")
                    else:
                        f.write(line)
        
        # Reload configuration
        reload_config()
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully'
        })
    except Exception as e:
        logger.error(f"Error updating source config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/destinations/<destination_name>/config', methods=['POST'])
def update_destination_config(destination_name):
    """Update destination configuration"""
    try:
        data = request.get_json()
        logger.info(f"API request: Updating config for destination '{destination_name}'")
        
        # Update environment variables
        import os
        if 'host' in data:
            os.environ['MYSQL_HOST'] = data['host']
        if 'port' in data:
            os.environ['MYSQL_PORT'] = str(data['port'])
        if 'user' in data:
            os.environ['MYSQL_USER'] = data['user']
        if 'password' in data:
            os.environ['MYSQL_PASSWORD'] = data['password']
        if 'database' in data:
            os.environ['MYSQL_DATABASE'] = data['database']
        
        # Update .env file
        env_path = '.env'
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith('MYSQL_HOST='):
                        f.write(f"MYSQL_HOST={data.get('host', 'mysql')}\n")
                    elif line.startswith('MYSQL_PORT='):
                        f.write(f"MYSQL_PORT={data.get('port', 3306)}\n")
                    elif line.startswith('MYSQL_USER='):
                        f.write(f"MYSQL_USER={data.get('user', 'eltuser')}\n")
                    elif line.startswith('MYSQL_PASSWORD='):
                        f.write(f"MYSQL_PASSWORD={data.get('password', '')}\n")
                    elif line.startswith('MYSQL_DATABASE='):
                        f.write(f"MYSQL_DATABASE={data.get('database', 'elt_data')}\n")
                    else:
                        f.write(line)
        
        # Reload configuration
        reload_config()
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully'
        })
    except Exception as e:
        logger.error(f"Error updating destination config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tables/available', methods=['GET'])
def get_available_tables():
    """Get available tables to sync"""
    try:
        # Get tables from config
        sources = config_manager.get_enabled_sources()
        tables = []
        
        for source in sources:
            sync_config = source.get('sync', {})
            source_tables = sync_config.get('tables', [])
            
            for table in source_tables:
                tables.append({
                    'name': table.get('name'),
                    'description': f"Tabla de {source.get('type')}",
                    'fields': table.get('fields', []),
                    'enabled': True,
                    'source': source.get('name')
                })
        
        return jsonify({
            'success': True,
            'data': tables
        })
    except Exception as e:
        logger.error(f"Error getting available tables: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tables/<table_name>/toggle', methods=['POST'])
def toggle_table(table_name):
    """Toggle table sync status"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        logger.info(f"API request: Toggle table '{table_name}' to {enabled}")
        
        # This would need to update the config file
        # For now, just return success
        # In production, you'd want to modify config.yaml
        
        return jsonify({
            'success': True,
            'message': f"Table '{table_name}' {'enabled' if enabled else 'disabled'}"
        })
    except Exception as e:
        logger.error(f"Error toggling table: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/stats', methods=['GET'])
def get_data_stats():
    """Get statistics of synced data"""
    try:
        stats = {}
        
        # Get destination config
        destinations = config_manager.get_destinations()
        if not destinations:
            return jsonify({'success': True, 'data': {}})
        
        dest = destinations[0]  # Use first destination
        from src.loaders import MySQLLoader
        
        loader = MySQLLoader(dest.get('config', {}))
        
        try:
            loader.connect()
            
            # Get list of tables
            cursor = loader.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for (table_name,) in tables:
                # Skip system tables
                if not table_name.startswith('facebook_ads_'):
                    continue
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                
                # Get last sync time
                try:
                    cursor.execute(f"SELECT MAX(_elt_loaded_at) FROM `{table_name}`")
                    last_sync = cursor.fetchone()[0]
                except:
                    last_sync = None
                
                stats[table_name] = {
                    'count': count,
                    'last_sync': last_sync.isoformat() if last_sync else None
                }
            
            cursor.close()
            loader.disconnect()
            
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            if loader.connection:
                loader.disconnect()
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error getting data stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/insights/config', methods=['GET', 'POST'])
def insights_config():
    """Get or update insights configuration"""
    try:
        if request.method == 'GET':
            # Get current insights config
            sources = config_manager.get_enabled_sources()
            insights_config = {}
            
            for source in sources:
                sync_config = source.get('sync', {})
                tables = sync_config.get('tables', [])
                
                for table in tables:
                    if table.get('name') == 'insights':
                        insights_config = {
                            'level': table.get('level', 'account'),
                            'date_range': table.get('date_range'),
                            'start_date': table.get('start_date'),
                            'end_date': table.get('end_date'),
                            'time_increment': table.get('time_increment', 'daily'),
                            'fields': table.get('fields', [])
                        }
            
            return jsonify({
                'success': True,
                'data': insights_config
            })
        
        else:  # POST
            data = request.get_json()
            logger.info("API request: Updating insights configuration")
            logger.info(f"Received data: {data}")
            
            # Update config.yaml
            with open(config_manager.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Find and update insights table config
            for source in config.get('sources', []):
                if source.get('type') == 'facebook_ads':
                    for table in source.get('sync', {}).get('tables', []):
                        if table.get('name') == 'insights':
                            table['level'] = data.get('level', 'account')
                            table['time_increment'] = data.get('time_increment', 'daily')
                            
                            # Si el usuario proporciona fechas específicas, usarlas
                            if data.get('start_date') and data.get('end_date'):
                                logger.info(f"Using date range: {data.get('start_date')} to {data.get('end_date')}")
                                table['start_date'] = data.get('start_date')
                                table['end_date'] = data.get('end_date')
                                # Remover date_range si está usando fechas específicas
                                table.pop('date_range', None)
                            else:
                                logger.info(f"Using days back: {data.get('date_range', 30)} days")
                                # Si no, usar date_range
                                table['date_range'] = data.get('date_range', 30)
                                # Remover start_date y end_date si está usando date_range
                                table.pop('start_date', None)
                                table.pop('end_date', None)
                            
                            if data.get('fields'):
                                logger.info(f"Updated fields: {len(data.get('fields'))} metrics")
                                table['fields'] = data.get('fields')
                            
                            logger.info(f"Final table config: level={table['level']}, time_increment={table['time_increment']}")
            
            # Write back to file
            with open(config_manager.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            # Reload configuration
            config_manager.reload()
            global orchestrator
            orchestrator = Orchestrator(config_manager)
            
            return jsonify({
                'success': True,
                'message': 'Insights configuration updated successfully'
            })
    
    except Exception as e:
        logger.error(f"Error managing insights config: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/insights/available-fields', methods=['GET'])
def insights_available_fields():
    """Get available fields for insights"""
    try:
        # Only metrics that are ACTUALLY valid for Facebook Ads Insights API
        # Based on: https://developers.facebook.com/docs/marketing-api/reference/ads-insights/
        available_fields = {
            'dimensions': {
                'account': {
                    'label': 'Nivel de Cuenta',
                    'description': 'Agregar todas las métricas a nivel de cuenta'
                },
                'campaign': {
                    'label': 'Por Campaña',
                    'description': 'Métricas desglosadas por cada campaña',
                    'fields': ['campaign_id', 'campaign_name']
                },
                'adset': {
                    'label': 'Por Conjunto de Anuncios',
                    'description': 'Métricas por cada conjunto de anuncios',
                    'fields': ['adset_id', 'adset_name', 'campaign_id']
                },
                'ad': {
                    'label': 'Por Anuncio Individual',
                    'description': 'Métricas por cada anuncio',
                    'fields': ['ad_id', 'ad_name', 'adset_id', 'campaign_id']
                }
            },
            'metrics': {
                # Métricas de Entrega
                'impressions': {'label': 'Impresiones', 'category': 'Entrega', 'description': 'Número de veces que se mostró el anuncio'},
                'clicks': {'label': 'Clics', 'category': 'Entrega', 'description': 'Número de clics en el anuncio'},
                'reach': {'label': 'Alcance', 'category': 'Entrega', 'description': 'Número único de personas que vieron el anuncio'},
                'frequency': {'label': 'Frecuencia', 'category': 'Entrega', 'description': 'Número promedio de veces que se mostró a cada persona'},
                
                # Métricas de Costo
                'spend': {'label': 'Gasto', 'category': 'Costo', 'description': 'Cantidad invertida'},
                'cpc': {'label': 'CPC', 'category': 'Costo', 'description': 'Costo por clic'},
                'cpm': {'label': 'CPM', 'category': 'Costo', 'description': 'Costo por mil impresiones'},
                'ctr': {'label': 'CTR', 'category': 'Costo', 'description': 'Tasa de clics (porcentaje)'},
                
                # Métricas de Conversión (válidas para Insights)
                'actions': {'label': 'Acciones', 'category': 'Conversión', 'description': 'Conversiones totales'},
                'conversion_rate_ranking': {'label': 'Ranking de Conv.', 'category': 'Conversión', 'description': 'Ranking de tasa de conversión'},
                'cost_per_action_type': {'label': 'Costo por Acción', 'category': 'Conversión', 'description': 'Costo promedio por tipo de acción'},
                'cost_per_conversion': {'label': 'Costo por Conversión', 'category': 'Conversión', 'description': 'Costo por cada conversión'},
                
                # Métricas de Valor
                'purchase_roas': {'label': 'ROAS (Compras)', 'category': 'Valor', 'description': 'Retorno sobre inversión en compras'},
                'roas': {'label': 'ROAS General', 'category': 'Valor', 'description': 'Retorno sobre inversión general'},
                'action_values': {'label': 'Valor de Acciones', 'category': 'Valor', 'description': 'Valor monetario de las acciones'},
                'conversion_values': {'label': 'Valor de Conversiones', 'category': 'Valor', 'description': 'Valor monetario de las conversiones'},
                
                # Métricas de Video (válidas para /insights endpoint)
                'video_play_actions': {'label': 'Reproducciones Video', 'category': 'Video', 'description': 'Acciones de reproducción de video'},
                'video_avg_time_watched_actions': {'label': 'Tiempo Promedio Video', 'category': 'Video', 'description': 'Tiempo promedio de video visto en segundos'},
                'video_15_sec_watched_actions': {'label': 'Video 15s Visto', 'category': 'Video', 'description': 'Reproducciones de más de 15 segundos'},
                'video_30_sec_watched_actions': {'label': 'Video 30s Visto', 'category': 'Video', 'description': 'Reproducciones de más de 30 segundos'},
                'video_continuous_2_sec_watched_actions': {'label': 'Video 2s Continuo', 'category': 'Video', 'description': 'Reproducciones continuas de 2+ segundos'},
                'video_thruplay_watched_actions': {'label': 'Thruplay Video', 'category': 'Video', 'description': 'Reproducciones hasta final'},
                
                # Métricas de Clics en Links (válidas para /insights)
                'inline_link_clicks': {'label': 'Clics en Enlace', 'category': 'Links', 'description': 'Clics en enlaces del anuncio'},
                'inline_link_click_ctr': {'label': 'CTR Enlace', 'category': 'Links', 'description': 'Tasa de clics en enlaces'},
                'cost_per_inline_link_click': {'label': 'Costo por Clic Enlace', 'category': 'Links', 'description': 'Costo promedio por clic en enlace'},
                
                # Métricas de Aplicación (válidas para /insights)
                'mobile_app_installs': {'label': 'Instalaciones App', 'category': 'Aplicación', 'description': 'Instalaciones de la aplicación'},
                'mobile_app_purchase_roas': {'label': 'ROAS Compras App', 'category': 'Aplicación', 'description': 'Retorno sobre inversión en compras dentro de app'},
                'app_store_clicks': {'label': 'Clics a Tienda App', 'category': 'Aplicación', 'description': 'Clics hacia la tienda de aplicaciones'},
            },
            'time_increments': {
                'daily': {'label': 'Diario', 'description': 'Un registro por día'},
                'monthly': {'label': 'Mensual', 'description': 'Un registro por mes'}
            }
        }
        
        return jsonify({
            'success': True,
            'data': available_fields
        })
    except Exception as e:
        logger.error(f"Error getting available fields: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/query', methods=['POST'])
def query_data():
    """Query data from a table with filters"""
    try:
        data = request.get_json()
        table_name = data.get('table')
        columns = data.get('columns', [])
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        filters = data.get('filters', {})
        limit = data.get('limit', 1000)
        
        if not table_name:
            return jsonify({
                'success': False,
                'error': 'Table name is required'
            }), 400
        
        # Get MySQL connection
        destinations = config_manager.get_destinations()
        if not destinations:
            return jsonify({
                'success': False,
                'error': 'No destination configured'
            }), 400
        
        from src.loaders import MySQLLoader
        loader = MySQLLoader(destinations[0].get('config', {}))
        loader.connect()
        
        try:
            cursor = loader.connection.cursor(dictionary=True)
            
            # Build SELECT clause
            if columns:
                select_clause = ', '.join([f'`{col}`' for col in columns])
            else:
                select_clause = '*'
            
            # Check if table has date columns
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'date_start'")
            has_date_columns = cursor.fetchone() is not None
            
            # Build WHERE clause
            where_conditions = []
            params = []
            
            # Date filters (only if table has date columns)
            if start_date and has_date_columns:
                where_conditions.append('`date_start` >= %s')
                params.append(start_date)
            
            if end_date and has_date_columns:
                where_conditions.append('`date_stop` <= %s')
                params.append(end_date)
            
            # Custom filters
            for field, value in filters.items():
                if value is not None and value != '':
                    where_conditions.append(f'`{field}` = %s')
                    params.append(value)
            
            # Build query
            query = f"SELECT {select_clause} FROM `{table_name}`"
            
            if where_conditions:
                query += ' WHERE ' + ' AND '.join(where_conditions)
            
            query += f' LIMIT {int(limit)}'
            
            logger.info(f"Executing query: {query}")
            logger.info(f"Parameters: {params}")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convert datetime objects to strings
            for row in results:
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row[key] = value.isoformat()
            
            cursor.close()
            loader.disconnect()
            
            return jsonify({
                'success': True,
                'data': results,
                'count': len(results)
            })
            
        except Exception as e:
            loader.disconnect()
            raise e
            
    except Exception as e:
        logger.error(f"Error querying data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/data/export', methods=['POST'])
def export_data():
    """Export data to CSV with filters"""
    try:
        import io
        import csv
        
        data = request.get_json()
        table_name = data.get('table')
        columns = data.get('columns', [])
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        filters = data.get('filters', {})
        
        if not table_name:
            return jsonify({
                'success': False,
                'error': 'Table name is required'
            }), 400
        
        # Get MySQL connection
        destinations = config_manager.get_destinations()
        if not destinations:
            return jsonify({
                'success': False,
                'error': 'No destination configured'
            }), 400
        
        from src.loaders import MySQLLoader
        loader = MySQLLoader(destinations[0].get('config', {}))
        loader.connect()
        
        try:
            cursor = loader.connection.cursor(dictionary=True)
            
            # Build SELECT clause
            if columns:
                select_clause = ', '.join([f'`{col}`' for col in columns])
            else:
                select_clause = '*'
            
            # Check if table has date columns
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'date_start'")
            has_date_columns = cursor.fetchone() is not None
            
            # Build WHERE clause
            where_conditions = []
            params = []
            
            # Date filters (only if table has date columns)
            if start_date and has_date_columns:
                where_conditions.append('`date_start` >= %s')
                params.append(start_date)
            
            if end_date and has_date_columns:
                where_conditions.append('`date_stop` <= %s')
                params.append(end_date)
            
            # Custom filters
            for field, value in filters.items():
                if value is not None and value != '':
                    where_conditions.append(f'`{field}` = %s')
                    params.append(value)
            
            # Build query
            query = f"SELECT {select_clause} FROM `{table_name}`"
            
            if where_conditions:
                query += ' WHERE ' + ' AND '.join(where_conditions)
            
            logger.info(f"Exporting data with query: {query}")
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            if not results:
                return jsonify({
                    'success': False,
                    'error': 'No data found with the specified filters'
                }), 404
            
            # Create CSV in memory
            output = io.StringIO()
            
            # Get column names from first row
            fieldnames = list(results[0].keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # Write data, converting datetime objects
            for row in results:
                row_data = {}
                for key, value in row.items():
                    if isinstance(value, datetime):
                        row_data[key] = value.isoformat()
                    else:
                        row_data[key] = value
                writer.writerow(row_data)
            
            cursor.close()
            loader.disconnect()
            
            # Prepare response
            output.seek(0)
            csv_data = output.getvalue()
            
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename={table_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                }
            )
            
        except Exception as e:
            loader.disconnect()
            raise e
            
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tables/<table_name>/columns', methods=['GET'])
def get_table_columns(table_name):
    """Get columns from a specific table"""
    try:
        destinations = config_manager.get_destinations()
        if not destinations:
            return jsonify({
                'success': False,
                'error': 'No destination configured'
            }), 400
        
        from src.loaders import MySQLLoader
        loader = MySQLLoader(destinations[0].get('config', {}))
        loader.connect()
        
        try:
            cursor = loader.connection.cursor()
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns_info = cursor.fetchall()
            
            columns = [{
                'name': col[0],
                'type': col[1],
                'nullable': col[2] == 'YES',
                'key': col[3],
                'default': col[4]
            } for col in columns_info]
            
            cursor.close()
            loader.disconnect()
            
            return jsonify({
                'success': True,
                'data': columns
            })
            
        except Exception as e:
            loader.disconnect()
            raise e
            
    except Exception as e:
        logger.error(f"Error getting table columns: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def run_api(host='0.0.0.0', port=5000):
    """Run the Flask API server"""
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    config_path = os.getenv('CONFIG_PATH', 'config/config.yaml')
    init_app(config_path)
    
    api_host = os.getenv('API_HOST', '0.0.0.0')
    api_port = int(os.getenv('API_PORT', 5000))
    
    logger.info(f"Starting Web API on {api_host}:{api_port}")
    run_api(host=api_host, port=api_port)
