#!/bin/bash
# Script para iniciar el sistema ELT con Docker

set -e

echo "🐳 Iniciando Sistema ELT con Docker"
echo "===================================="
echo ""

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "   Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar si Docker Compose está disponible
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    exit 1
fi

# Determinar el comando de Docker Compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Verificar si existe archivo .env
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env desde .env.docker..."
    cp .env.docker .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de Facebook Ads"
    echo "   Especialmente estos valores:"
    echo "   - FACEBOOK_APP_ID"
    echo "   - FACEBOOK_APP_SECRET"
    echo "   - FACEBOOK_ACCESS_TOKEN"
    echo "   - FACEBOOK_AD_ACCOUNT_ID"
    echo ""
    read -p "Presiona Enter cuando hayas configurado el archivo .env..."
fi

# Crear directorio de logs si no existe
mkdir -p logs

echo "🏗️  Construyendo imágenes Docker..."
$DOCKER_COMPOSE build

echo ""
echo "🚀 Iniciando contenedores..."
$DOCKER_COMPOSE up -d mysql elt-api

echo ""
echo "⏳ Esperando a que MySQL esté listo..."
sleep 10

echo ""
echo "✅ Sistema ELT iniciado correctamente!"
echo ""
echo "📊 Servicios disponibles:"
echo "   - API Web: http://localhost:5000"
echo "   - MySQL: localhost:3306"
echo ""
echo "📋 Comandos útiles:"
echo "   Ver logs:              $DOCKER_COMPOSE logs -f"
echo "   Ver logs de API:       $DOCKER_COMPOSE logs -f elt-api"
echo "   Ver logs de MySQL:     $DOCKER_COMPOSE logs -f mysql"
echo "   Detener servicios:     $DOCKER_COMPOSE down"
echo "   Reiniciar servicios:   $DOCKER_COMPOSE restart"
echo ""
echo "🔄 Para iniciar también el worker de sincronización automática:"
echo "   $DOCKER_COMPOSE --profile worker up -d"
echo ""
