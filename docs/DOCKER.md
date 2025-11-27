# Documentación Docker - Sistema ELT

## Tabla de Contenidos

- [Inicio Rápido](#inicio-rápido)
- [Arquitectura](#arquitectura)
- [Servicios](#servicios)
- [Configuración](#configuración)
- [Comandos](#comandos)
- [Desarrollo](#desarrollo)
- [Producción](#producción)
- [Troubleshooting](#troubleshooting)

## Inicio Rápido

### Método 1: Script automatizado
```bash
./docker-start.sh
```

### Método 2: Docker Compose
```bash
docker-compose up -d
```

### Método 3: Makefile
```bash
make install
```

## Arquitectura

```
┌──────────────────────────────────────────────────┐
│                    Red Docker                     │
│  elt-network (bridge)                            │
│                                                   │
│  ┌─────────────┐    ┌──────────────┐            │
│  │             │    │              │            │
│  │   MySQL     │◄───│   ELT-API    │            │
│  │   :3306     │    │   :5000      │            │
│  │             │    │              │            │
│  └──────┬──────┘    └──────────────┘            │
│         │                                         │
│         │           ┌──────────────┐            │
│         │           │              │            │
│         └───────────│  ELT-Worker  │            │
│                     │  (opcional)  │            │
│                     │              │            │
│                     └──────────────┘            │
│                                                   │
└──────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
    Puerto 3306          Puerto 5000
    (MySQL)              (Web UI)
```

## Servicios

### 1. MySQL (Base de datos)
- **Imagen**: `mysql:8.0`
- **Puerto**: 3306
- **Base de datos**: elt_data
- **Volumen**: `mysql_data` (persistente)
- **Health check**: Verifica cada 10s

### 2. ELT-API (Servidor Web)
- **Build**: `Dockerfile`
- **Puerto**: 5000
- **Depende de**: MySQL (espera health check)
- **Volúmenes**:
  - `./config` → `/app/config`
  - `./logs` → `/app/logs`

### 3. ELT-Worker (Sincronización)
- **Build**: `Dockerfile`
- **Sin puerto expuesto**
- **Profile**: `worker` (opcional)
- **Comando**: `python main.py --mode scheduled`

## Configuración

### Variables de Entorno

Archivo `.env`:

```env
# MySQL
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=eltuser
MYSQL_PASSWORD=eltpassword
MYSQL_DATABASE=elt_data

# Facebook Ads (REQUERIDO)
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_AD_ACCOUNT_ID=act_your_account_id

# API
API_HOST=0.0.0.0
API_PORT=5000
```

### Cambiar Puertos

Editar `.env`:
```env
API_PORT=8080  # Cambia puerto externo
MYSQL_PORT=3307  # Cambia puerto MySQL
```

O editar `docker-compose.yml`:
```yaml
services:
  elt-api:
    ports:
      - "8080:5000"  # host:container
```

## Comandos

### Usando Makefile (Recomendado)

```bash
make help          # Ver todos los comandos
make install       # Instalación completa
make up            # Iniciar servicios
make down          # Detener servicios
make logs          # Ver logs
make restart       # Reiniciar
make status        # Ver estado
make clean         # Limpiar todo
make run-pipeline  # Ejecutar pipeline
make backup-db     # Backup de MySQL
```

### Usando Docker Compose

```bash
# Iniciar
docker-compose up -d

# Iniciar con worker
docker-compose --profile worker up -d

# Detener
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar servicio
docker-compose restart elt-api

# Ver estado
docker-compose ps

# Ejecutar comando en contenedor
docker-compose exec elt-api python main.py --mode once

# Shell en contenedor
docker-compose exec elt-api bash
```

### Usando Scripts

```bash
./docker-start.sh          # Iniciar
./docker-stop.sh           # Detener
./docker-run-pipeline.sh   # Ejecutar pipeline
```

## Desarrollo

### Modo Desarrollo con Hot Reload

```bash
# Usar docker-compose.dev.yml
docker-compose -f docker-compose.dev.yml up

# O con Make
make dev-up
```

**Características**:
- ✅ Hot reload automático
- ✅ Código montado como volumen
- ✅ Debug habilitado
- ✅ Logs en tiempo real

### Estructura de Desarrollo

```bash
.
├── Dockerfile              # Producción
├── Dockerfile.dev          # Desarrollo
├── docker-compose.yml      # Producción
└── docker-compose.dev.yml  # Desarrollo
```

## Producción

### Build y Deploy

```bash
# Build
docker-compose build --no-cache

# Iniciar en background
docker-compose up -d

# Verificar
docker-compose ps
docker-compose logs --tail=50
```

### Health Checks

MySQL incluye health check automático:
```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Backups

```bash
# Backup automático
make backup-db

# Backup manual
docker-compose exec -T mysql mysqldump -u eltuser -peltpassword elt_data > backup.sql

# Restaurar
make restore-db FILE=backup.sql
```

## Troubleshooting

### MySQL no inicia

```bash
# Ver logs
docker-compose logs mysql

# Reiniciar
docker-compose restart mysql

# Recrear
docker-compose down
docker-compose up -d
```

### Error: "Cannot connect to MySQL"

```bash
# Verificar health check
docker-compose ps

# Esperar a que esté healthy
docker-compose logs -f mysql

# Verificar conexión
docker-compose exec mysql mysql -u eltuser -peltpassword -e "SELECT 1"
```

### API no responde

```bash
# Ver logs
docker-compose logs elt-api

# Reiniciar
docker-compose restart elt-api

# Verificar puerto
netstat -an | grep 5000
```

### Puerto ocupado

```bash
# Cambiar puerto en .env
API_PORT=8080

# Reiniciar
docker-compose down
docker-compose up -d
```

### Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar todo
docker-compose down -v

# Eliminar imágenes
docker rmi eltmko-elt-api

# Reconstruir
docker-compose build --no-cache
docker-compose up -d
```

### Ver logs detallados

```bash
# Últimas 100 líneas
docker-compose logs --tail=100

# Seguir logs
docker-compose logs -f

# Solo errores (aproximado)
docker-compose logs | grep -i error
```

### Conectar a MySQL desde host

```bash
mysql -h 127.0.0.1 -P 3306 -u eltuser -peltpassword elt_data
```

### Ejecutar comandos en contenedores

```bash
# Python shell
docker-compose exec elt-api python

# Bash
docker-compose exec elt-api bash

# MySQL client
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data

# Ver archivos
docker-compose exec elt-api ls -la /app
```

### Actualizar código sin rebuild

En desarrollo (con volúmenes montados):
```bash
# Solo reiniciar
docker-compose restart elt-api
```

En producción:
```bash
# Rebuild necesario
docker-compose build elt-api
docker-compose up -d elt-api
```

### Verificar volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar
docker volume inspect eltmko_mysql_data

# Eliminar volumen
docker volume rm eltmko_mysql_data
```

### Problemas de permisos

```bash
# Dar permisos a logs
chmod -R 777 logs/

# Cambiar owner (Linux)
sudo chown -R $USER:$USER logs/
```

## Comandos Útiles Adicionales

### Monitoreo

```bash
# Ver uso de recursos
docker stats

# Inspeccionar contenedor
docker inspect eltmko-api

# Ver procesos en contenedor
docker-compose exec elt-api ps aux
```

### Networking

```bash
# Listar redes
docker network ls

# Inspeccionar red
docker network inspect eltmko_elt-network

# Probar conectividad
docker-compose exec elt-api ping mysql
```

### Limpieza

```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune

# Limpiar todo
docker system prune -a --volumes
```

## Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MySQL Docker Image](https://hub.docker.com/_/mysql)

---

**Última actualización**: Noviembre 2025
