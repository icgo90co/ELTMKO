#!/bin/bash
# Script de inicio rápido para el sistema ELT

echo "🚀 Configurando Sistema ELT..."

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Copiar archivo de ejemplo .env si no existe
if [ ! -f ".env" ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor edita el archivo .env con tus credenciales"
fi

# Crear directorio de logs
mkdir -p logs

echo ""
echo "✅ Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Editar .env con tus credenciales"
echo "2. Editar config/config.yaml si es necesario"
echo "3. Ejecutar el sistema:"
echo "   - Ejecución única: python main.py --mode once"
echo "   - Modo programado: python main.py --mode scheduled"
echo "   - Interfaz web: python api.py"
echo ""
