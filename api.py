"""
Web API for ELT System Configuration
Provides REST endpoints to manage sources, destinations, and pipelines
"""
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
CORS(app)

# Global variables
config_manager = None
orchestrator = None


def init_app(config_path: str = "config/config.yaml"):
    """Initialize the application"""
    global config_manager, orchestrator
    
    config_manager = ConfigManager(config_path)
    setup_logger(config_manager.get_logging_config())
    orchestrator = Orchestrator(config_manager)
    
    logger.info("Web API initialized")


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
