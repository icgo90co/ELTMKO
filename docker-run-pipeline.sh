#!/bin/bash
# Script para ejecutar un pipeline manualmente usando Docker

set -e

# Determinar el comando de Docker Compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

if [ -z "$1" ]; then
    echo "🔄 Ejecutando todos los pipelines..."
    $DOCKER_COMPOSE run --rm elt-api python main.py --mode once
else
    echo "🔄 Ejecutando pipeline: $1"
    $DOCKER_COMPOSE run --rm elt-api python -c "
from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator

config_manager = ConfigManager('config/config.yaml')
setup_logger(config_manager.get_logging_config())
orchestrator = Orchestrator(config_manager)
result = orchestrator.run_source('$1')
print(result)
"
fi

echo ""
echo "✅ Pipeline ejecutado"
echo ""
