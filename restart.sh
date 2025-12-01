#!/bin/bash
# Script para reiniciar contenedores SIN perder datos

echo "🔄 Reiniciando contenedores (manteniendo datos)..."
docker-compose restart

echo "✅ Contenedores reiniciados"
echo "📊 Logs de la API:"
docker logs eltmko-api --tail 20
