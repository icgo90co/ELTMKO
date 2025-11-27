#!/bin/bash
# Script de verificación del sistema Docker

set -e

echo "🔍 Verificando Sistema ELT Docker"
echo "=================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para checks
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 está instalado"
        return 0
    else
        echo -e "${RED}✗${NC} $1 NO está instalado"
        return 1
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 existe"
        return 0
    else
        echo -e "${RED}✗${NC} $1 NO existe"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 existe"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 NO existe (se creará automáticamente)"
        return 1
    fi
}

ERRORS=0

# Verificar comandos
echo "📦 Verificando herramientas..."
check_command docker || ERRORS=$((ERRORS+1))
if command -v docker-compose &> /dev/null; then
    check_command docker-compose
elif docker compose version &> /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} docker compose está disponible"
else
    echo -e "${RED}✗${NC} docker-compose NO está disponible"
    ERRORS=$((ERRORS+1))
fi

echo ""

# Verificar archivos necesarios
echo "📄 Verificando archivos necesarios..."
check_file "Dockerfile" || ERRORS=$((ERRORS+1))
check_file "docker-compose.yml" || ERRORS=$((ERRORS+1))
check_file "requirements.txt" || ERRORS=$((ERRORS+1))
check_file "main.py" || ERRORS=$((ERRORS+1))
check_file "api.py" || ERRORS=$((ERRORS+1))

echo ""

# Verificar configuración
echo "⚙️  Verificando configuración..."
check_file ".env.docker" || ERRORS=$((ERRORS+1))

if check_file ".env"; then
    # Verificar que .env tenga las variables necesarias
    if grep -q "FACEBOOK_APP_ID=your_app_id" .env; then
        echo -e "${YELLOW}⚠${NC} .env contiene valores de ejemplo. Actualiza con credenciales reales."
    else
        echo -e "${GREEN}✓${NC} .env parece configurado"
    fi
else
    echo -e "${YELLOW}⚠${NC} .env no existe. Créalo con: cp .env.docker .env"
fi

check_file "config/config.yaml" || ERRORS=$((ERRORS+1))

echo ""

# Verificar directorios
echo "📁 Verificando estructura..."
check_dir "src"
check_dir "src/core"
check_dir "src/extractors"
check_dir "src/loaders"
check_dir "config"
check_dir "static"
check_dir "logs"

echo ""

# Verificar Docker daemon
echo "🐳 Verificando Docker daemon..."
if docker info &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker daemon está corriendo"
else
    echo -e "${RED}✗${NC} Docker daemon NO está corriendo"
    echo "   Inicia Docker Desktop o ejecuta: sudo systemctl start docker"
    ERRORS=$((ERRORS+1))
fi

echo ""

# Verificar puertos
echo "🔌 Verificando puertos..."
if command -v netstat &> /dev/null; then
    if netstat -tuln | grep -q ":5000 "; then
        echo -e "${YELLOW}⚠${NC} Puerto 5000 está en uso"
        echo "   Puedes cambiar el puerto en .env (API_PORT)"
    else
        echo -e "${GREEN}✓${NC} Puerto 5000 está disponible"
    fi
    
    if netstat -tuln | grep -q ":3306 "; then
        echo -e "${YELLOW}⚠${NC} Puerto 3306 está en uso"
        echo "   Puedes cambiar el puerto en .env (MYSQL_PORT)"
    else
        echo -e "${GREEN}✓${NC} Puerto 3306 está disponible"
    fi
else
    echo -e "${YELLOW}⚠${NC} netstat no disponible, no se pueden verificar puertos"
fi

echo ""
echo "=================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Todas las verificaciones pasaron!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Asegúrate de configurar .env con tus credenciales"
    echo "2. Ejecuta: ./docker-start.sh"
    echo "3. Abre: http://localhost:5000"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERRORS problema(s)${NC}"
    echo ""
    echo "Por favor corrige los errores antes de continuar."
    exit 1
fi
