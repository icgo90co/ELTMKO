# Cheat Sheet - Comandos Docker del Sistema ELT

## 🚀 Inicio y Parada

```bash
# Iniciar sistema completo
./docker-start.sh

# Iniciar con Makefile
make install

# Iniciar manualmente
docker-compose up -d

# Detener sistema
./docker-stop.sh
# o
docker-compose down

# Reiniciar
docker-compose restart
```

## 📊 Monitoreo

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de API
docker-compose logs -f elt-api

# Ver logs solo de MySQL
docker-compose logs -f mysql

# Ver últimas 50 líneas
docker-compose logs --tail=50

# Ver uso de recursos
docker stats
```

## 🔄 Ejecutar Pipelines

```bash
# Ejecutar todos los pipelines
./docker-run-pipeline.sh

# Ejecutar con make
make run-pipeline

# Ejecutar manualmente
docker-compose run --rm elt-api python main.py --mode once

# Iniciar worker de sincronización automática
docker-compose --profile worker up -d
```

## 🐚 Acceso a Contenedores

```bash
# Shell en contenedor de API
docker-compose exec elt-api bash

# Shell Python
docker-compose exec elt-api python

# MySQL client
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data

# Ver archivos
docker-compose exec elt-api ls -la /app
```

## 🔧 Configuración

```bash
# Editar configuración
nano config/config.yaml

# Editar variables de entorno
nano .env

# Recargar configuración (reiniciar API)
docker-compose restart elt-api

# Ver configuración actual
docker-compose exec elt-api cat config/config.yaml
```

## 💾 Base de Datos

```bash
# Conectar a MySQL desde host
mysql -h 127.0.0.1 -P 3306 -u eltuser -peltpassword elt_data

# Backup de base de datos
docker-compose exec -T mysql mysqldump -u eltuser -peltpassword elt_data > backup.sql
# o
make backup-db

# Restaurar backup
docker-compose exec -T mysql mysql -u eltuser -peltpassword elt_data < backup.sql
# o
make restore-db FILE=backup.sql

# Ver tablas
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data -e "SHOW TABLES"

# Ver datos de una tabla
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data -e "SELECT * FROM facebook_ads_campaigns LIMIT 10"
```

## 🏗️ Build y Desarrollo

```bash
# Reconstruir imágenes
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Modo desarrollo (hot-reload)
docker-compose -f docker-compose.dev.yml up

# Ver imágenes
docker images | grep eltmko
```

## 🧹 Limpieza

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar contenedores y volúmenes (⚠️ borra datos)
docker-compose down -v

# Limpiar todo Docker
make prune
# o
docker system prune -a --volumes

# Eliminar solo volumen de MySQL
docker volume rm eltmko_mysql_data
```

## 🔍 Debugging

```bash
# Ver configuración de contenedor
docker inspect eltmko-api

# Ver logs de errores
docker-compose logs | grep -i error

# Verificar conectividad entre contenedores
docker-compose exec elt-api ping mysql

# Ver procesos en contenedor
docker-compose exec elt-api ps aux

# Ver variables de entorno
docker-compose exec elt-api env
```

## 📦 Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect eltmko_mysql_data

# Ver tamaño de volumen
docker system df -v
```

## 🌐 Red

```bash
# Listar redes
docker network ls

# Inspeccionar red
docker network inspect eltmko_elt-network

# Ver IPs de contenedores
docker-compose exec elt-api hostname -I
```

## 🆘 Troubleshooting Rápido

```bash
# MySQL no inicia
docker-compose down -v
docker-compose up -d mysql
docker-compose logs -f mysql

# API no responde
docker-compose restart elt-api
docker-compose logs -f elt-api

# Puerto ocupado
# Editar .env y cambiar API_PORT o MYSQL_PORT
docker-compose down
docker-compose up -d

# Resetear todo
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Tareas Comunes

### Cambiar puerto de la API
```bash
echo "API_PORT=8080" >> .env
docker-compose down
docker-compose up -d
```

### Ver datos extraídos
```bash
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data -e "
SELECT 
    COUNT(*) as total_campaigns,
    MAX(_elt_loaded_at) as last_sync
FROM facebook_ads_campaigns
"
```

### Ejecutar pipeline específico
```bash
docker-compose run --rm elt-api python -c "
from src.core import ConfigManager, setup_logger
from src.orchestrator import Orchestrator
config = ConfigManager('config/config.yaml')
setup_logger(config.get_logging_config())
orch = Orchestrator(config)
result = orch.run_source('facebook_ads')
print(result)
"
```

### Ver espacio usado
```bash
docker system df
```

### Actualizar código sin rebuild (desarrollo)
```bash
# El código se actualiza automáticamente con volúmenes montados
docker-compose -f docker-compose.dev.yml restart elt-api
```

## 📚 Ayuda

```bash
# Ver ayuda de Makefile
make help

# Ver ayuda de docker-compose
docker-compose --help

# Ver versión de Docker
docker --version
docker-compose --version
```

---

**Tip**: Agrega alias a tu `.bashrc` o `.zshrc`:

```bash
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcp='docker-compose ps'
alias dcr='docker-compose restart'
```
