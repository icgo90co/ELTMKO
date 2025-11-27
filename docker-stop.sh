#!/bin/bash
# Script para detener el sistema ELT

set -e

echo "🛑 Deteniendo Sistema ELT..."

# Determinar el comando de Docker Compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Detener y eliminar contenedores
$DOCKER_COMPOSE down

echo ""
echo "✅ Sistema ELT detenido"
echo ""
echo "💡 Nota: Los datos de MySQL se conservan en el volumen 'mysql_data'"
echo "   Para eliminar también los datos: $DOCKER_COMPOSE down -v"
echo ""
