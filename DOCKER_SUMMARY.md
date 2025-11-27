# 🐳 Sistema ELT con Docker - Resumen de Implementación

## ✅ Archivos Docker Creados

### Configuración Principal
- ✅ `Dockerfile` - Imagen de producción
- ✅ `Dockerfile.dev` - Imagen de desarrollo con hot-reload
- ✅ `docker-compose.yml` - Orquestación de servicios (producción)
- ✅ `docker-compose.dev.yml` - Orquestación para desarrollo
- ✅ `.dockerignore` - Archivos excluidos del build
- ✅ `.env.docker` - Variables de entorno de ejemplo
- ✅ `init-db.sql` - Script de inicialización de MySQL

### Scripts de Utilidad
- ✅ `docker-start.sh` - Iniciar sistema completo
- ✅ `docker-stop.sh` - Detener sistema
- ✅ `docker-run-pipeline.sh` - Ejecutar pipelines manualmente
- ✅ `docker-verify.sh` - Verificar configuración del sistema

### Automatización
- ✅ `Makefile` - Comandos simplificados (make install, make up, etc.)

### Documentación
- ✅ `docs/DOCKER.md` - Documentación completa de Docker
- ✅ `DOCKER_QUICKSTART.md` - Guía de inicio rápido
- ✅ `DOCKER_README.md` - Resumen de comandos
- ✅ `DOCKER_CHEATSHEET.md` - Cheat sheet de comandos útiles
- ✅ `README.md` - Actualizado con sección Docker

## 🏗️ Arquitectura Implementada

```
┌─────────────────────────────────────────────────────┐
│                Docker Network (elt-network)          │
│                                                      │
│  ┌──────────────┐         ┌──────────────┐         │
│  │              │         │              │         │
│  │    MySQL     │◄────────│   ELT-API    │         │
│  │   :3306      │         │   :5000      │         │
│  │              │         │              │         │
│  └──────┬───────┘         └──────────────┘         │
│         │                                            │
│         │                 ┌──────────────┐         │
│         │                 │              │         │
│         └─────────────────│  ELT-Worker  │         │
│                           │  (opcional)  │         │
│                           │              │         │
│                           └──────────────┘         │
│                                                      │
└─────────────────────────────────────────────────────┘
         │                         │
         ▼                         ▼
    localhost:3306          localhost:5000
      (MySQL)               (Web Interface)
```

## 📦 Servicios Docker

### 1. MySQL (Base de datos)
- **Imagen**: mysql:8.0
- **Puerto**: 3306
- **Volumen**: mysql_data (persistente)
- **Health Check**: Verifica disponibilidad cada 10s
- **Credenciales por defecto**:
  - Usuario: eltuser
  - Contraseña: eltpassword
  - Base de datos: elt_data

### 2. ELT-API (Servidor Web + API REST)
- **Build**: Dockerfile personalizado
- **Puerto**: 5000
- **Funciones**:
  - Interfaz web de control
  - API REST para gestión
  - Ejecución manual de pipelines
- **Volúmenes montados**:
  - `./config` → Configuración
  - `./logs` → Logs del sistema

### 3. ELT-Worker (Sincronización Automática)
- **Build**: Dockerfile personalizado
- **Perfil**: worker (opcional)
- **Función**: Ejecuta pipelines según intervalos configurados
- **Comando**: `python main.py --mode scheduled`

## 🚀 Formas de Iniciar el Sistema

### Opción 1: Script Automatizado (Recomendado)
```bash
./docker-start.sh
```
**Ventajas**: Verificaciones automáticas, mensajes informativos

### Opción 2: Makefile
```bash
make install    # Primera vez
make up         # Subsecuentes
```
**Ventajas**: Comandos cortos y fáciles de recordar

### Opción 3: Docker Compose Directo
```bash
docker-compose up -d
```
**Ventajas**: Control total, estándar de Docker

### Opción 4: Con Worker Automático
```bash
docker-compose --profile worker up -d
```
**Ventajas**: Sincronización automática continua

## 📋 Comandos Esenciales

```bash
# Iniciar
./docker-start.sh

# Ver logs
docker-compose logs -f

# Estado
docker-compose ps

# Detener
./docker-stop.sh

# Ejecutar pipeline
./docker-run-pipeline.sh

# Reiniciar
docker-compose restart

# Limpiar todo
docker-compose down -v
```

## 🔧 Configuración Requerida

### 1. Variables de Entorno (.env)
```env
# MySQL (valores por defecto funcionan)
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=eltuser
MYSQL_PASSWORD=eltpassword
MYSQL_DATABASE=elt_data

# Facebook Ads (REQUERIDO - actualizar con valores reales)
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
FACEBOOK_ACCESS_TOKEN=tu_access_token
FACEBOOK_AD_ACCOUNT_ID=act_tu_account_id

# API (valores por defecto funcionan)
API_HOST=0.0.0.0
API_PORT=5000
```

### 2. Configuración de Pipelines (config/config.yaml)
Ya está configurado por defecto, pero se puede personalizar:
- Fuentes de datos (sources)
- Destinos (destinations)
- Tablas a sincronizar
- Intervalos de sincronización

## 🎯 Casos de Uso

### Desarrollo
```bash
# Usar docker-compose.dev.yml para hot-reload
docker-compose -f docker-compose.dev.yml up
```

### Producción
```bash
# Usar docker-compose.yml normal
docker-compose up -d
```

### CI/CD
```bash
# Build
docker-compose build --no-cache

# Test
docker-compose run --rm elt-api python -m pytest

# Deploy
docker-compose up -d
```

## 💾 Persistencia de Datos

### Volúmenes Docker
- **mysql_data**: Todos los datos de la base de datos
- **./config**: Archivos de configuración (montado)
- **./logs**: Logs del sistema (montado)

### Backups
```bash
# Backup automático
make backup-db

# Manual
docker-compose exec -T mysql mysqldump -u eltuser -peltpassword elt_data > backup.sql

# Restaurar
make restore-db FILE=backup.sql
```

## 🔍 Verificación del Sistema

```bash
# Ejecutar verificación completa
./docker-verify.sh

# Verificar servicios corriendo
docker-compose ps

# Verificar conectividad
docker-compose exec elt-api ping mysql

# Verificar logs
docker-compose logs --tail=50
```

## 🌐 Acceso a Servicios

| Servicio | URL/Host | Puerto |
|----------|----------|--------|
| Interfaz Web | http://localhost:5000 | 5000 |
| API REST | http://localhost:5000/api | 5000 |
| MySQL (externo) | localhost:3306 | 3306 |
| MySQL (interno) | mysql:3306 | 3306 |

## 🆘 Solución de Problemas Comunes

### Puerto ocupado
```bash
# Cambiar en .env
API_PORT=8080
MYSQL_PORT=3307
```

### MySQL no inicia
```bash
docker-compose down -v
docker-compose up -d
```

### Ver errores
```bash
docker-compose logs | grep -i error
```

### Resetear completamente
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Documentación

- **Guía Completa**: `docs/DOCKER.md`
- **Quick Start**: `DOCKER_QUICKSTART.md`
- **Comandos útiles**: `DOCKER_CHEATSHEET.md`
- **README Principal**: `README.md`

## ✨ Características Docker

- ✅ **Autocontenido**: Todo incluido (app + MySQL)
- ✅ **Portable**: Funciona en cualquier OS con Docker
- ✅ **Fácil de usar**: Scripts automatizados
- ✅ **Desarrollo friendly**: Hot-reload disponible
- ✅ **Producción ready**: Health checks y restart policies
- ✅ **Persistencia**: Volúmenes para datos
- ✅ **Networking**: Red aislada para los servicios
- ✅ **Escalable**: Fácil agregar más workers

## 🎉 Próximos Pasos

1. ✅ **Configurar credenciales**: Editar `.env`
2. ✅ **Iniciar sistema**: `./docker-start.sh`
3. ✅ **Abrir interfaz**: http://localhost:5000
4. ✅ **Ejecutar primer pipeline**: Desde la interfaz web
5. ✅ **Verificar datos**: Revisar tablas en MySQL

---

**Sistema completamente dockerizado y listo para producción** 🚀

_Última actualización: Noviembre 2025_
