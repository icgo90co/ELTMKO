#!/bin/bash
# Script de inicio completo - ejecuta todo en orden

clear

cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║     🚀 Sistema ELT - Inicio Completo con Docker          ║
╚═══════════════════════════════════════════════════════════╝

Este script ejecutará el sistema ELT completo en Docker.
Se encargará de:
  ✓ Verificar requisitos
  ✓ Configurar variables de entorno
  ✓ Construir imágenes Docker
  ✓ Iniciar servicios (MySQL + API)
  ✓ Verificar funcionamiento

EOF

echo "¿Deseas continuar? (s/n)"
read -r response

if [[ ! "$response" =~ ^[Ss]$ ]]; then
    echo "❌ Instalación cancelada"
    exit 0
fi

echo ""
echo "🔍 Paso 1/5: Verificando sistema..."
./docker-verify.sh
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Verificación falló. Por favor corrige los errores."
    exit 1
fi

echo ""
echo "⚙️  Paso 2/5: Verificando configuración..."
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.docker .env
    echo ""
    echo "⚠️  IMPORTANTE: Debes editar .env con tus credenciales de Facebook Ads"
    echo ""
    echo "Presiona Enter para abrir el editor, o Ctrl+C para salir y editar manualmente"
    read
    ${EDITOR:-nano} .env
fi

echo ""
echo "🏗️  Paso 3/5: Construyendo imágenes Docker..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Error al construir imágenes"
    exit 1
fi

echo ""
echo "🚀 Paso 4/5: Iniciando servicios..."
docker-compose up -d mysql elt-api

if [ $? -ne 0 ]; then
    echo "❌ Error al iniciar servicios"
    exit 1
fi

echo ""
echo "⏳ Esperando que los servicios estén listos..."
sleep 15

echo ""
echo "✅ Paso 5/5: Verificando servicios..."

# Verificar que los contenedores estén corriendo
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Los servicios no están corriendo correctamente"
    echo "Ver logs con: docker-compose logs"
    exit 1
fi

# Verificar API
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✅ API funcionando correctamente"
else
    echo "⚠️  API no responde aún, puede tardar unos segundos más"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✅ INSTALACIÓN COMPLETADA                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Estado de servicios:"
docker-compose ps
echo ""
echo "🌐 Servicios disponibles:"
echo "   • Interfaz Web:  http://localhost:5000"
echo "   • API REST:      http://localhost:5000/api"
echo "   • MySQL:         localhost:3306"
echo ""
echo "📋 Comandos útiles:"
echo "   • Ver logs:           docker-compose logs -f"
echo "   • Detener:            ./docker-stop.sh"
echo "   • Ejecutar pipeline:  ./docker-run-pipeline.sh"
echo "   • Ver estado:         docker-compose ps"
echo "   • Ayuda completa:     make help"
echo ""
echo "📖 Documentación:"
echo "   • Inicio rápido:  DOCKER_QUICKSTART.md"
echo "   • Comandos:       DOCKER_CHEATSHEET.md"
echo "   • Índice:         DOCUMENTATION_INDEX.md"
echo ""
echo "🎉 ¡Listo! Abre http://localhost:5000 en tu navegador"
echo ""
EOF
