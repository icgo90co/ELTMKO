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
