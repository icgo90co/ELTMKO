# Guía de Inicio Rápido con Docker 🐳

Esta guía te ayudará a levantar el sistema ELT en menos de 5 minutos usando Docker.

## Requisitos

- Docker instalado ([Instalar Docker](https://docs.docker.com/get-docker/))
- Docker Compose instalado (viene con Docker Desktop)

## Pasos

### 1. Configurar credenciales

```bash
# Copiar archivo de ejemplo
cp .env.docker .env

# Editar con tus credenciales de Facebook Ads
nano .env  # o usar tu editor favorito
```

**Importante**: Actualiza estos valores en `.env`:
- `FACEBOOK_APP_ID`
- `FACEBOOK_APP_SECRET`
- `FACEBOOK_ACCESS_TOKEN`
- `FACEBOOK_AD_ACCOUNT_ID`

### 2. Iniciar el sistema

```bash
./docker-start.sh
```

Este script:
- ✅ Construye las imágenes Docker
- ✅ Inicia MySQL
- ✅ Inicia la API web
- ✅ Configura la red y volúmenes

### 3. Acceder a la interfaz

Abre tu navegador en: **http://localhost:5000**

## Comandos Útiles

### Ver estado de contenedores
```bash
docker-compose ps
```

### Ver logs
```bash
# Todos los logs
docker-compose logs -f

# Solo API
docker-compose logs -f elt-api

# Solo MySQL
docker-compose logs -f mysql
```

### Ejecutar pipeline manualmente
```bash
./docker-run-pipeline.sh
```

### Reiniciar servicios
```bash
docker-compose restart
```

### Detener sistema
```bash
./docker-stop.sh
# o
docker-compose down
```

### Eliminar todo (incluyendo datos)
```bash
docker-compose down -v
```

## Servicios Disponibles

| Servicio | Puerto | URL |
|----------|--------|-----|
| API Web | 5000 | http://localhost:5000 |
| MySQL | 3306 | localhost:3306 |

## Credenciales MySQL (por defecto)

- **Host**: localhost (desde fuera) o `mysql` (desde contenedores)
- **Puerto**: 3306
- **Usuario**: eltuser
- **Contraseña**: eltpassword
- **Base de datos**: elt_data

## Iniciar con Worker Automático

Para sincronización continua:

```bash
docker-compose --profile worker up -d
```

Este comando adicional inicia un contenedor que ejecuta pipelines automáticamente según los intervalos configurados en `config/config.yaml`.

## Estructura de Volúmenes

Los datos se persisten en:

- **mysql_data**: Base de datos MySQL (persiste entre reinicios)
- **./config**: Archivos de configuración
- **./logs**: Logs del sistema

## Solución Rápida de Problemas

### MySQL no inicia
```bash
docker-compose down -v
docker-compose up -d
```

### Ver errores
```bash
docker-compose logs --tail=50
```

### Reconstruir imágenes
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Conectar a MySQL desde terminal
```bash
docker-compose exec mysql mysql -u eltuser -peltpassword elt_data
```

## Próximos Pasos

1. ✅ Verifica que los servicios estén corriendo: `docker-compose ps`
2. ✅ Abre la interfaz web: http://localhost:5000
3. ✅ Ejecuta tu primer pipeline desde la interfaz
4. ✅ Revisa los datos en MySQL

## ¿Necesitas ayuda?

- Ver README principal: `README.md`
- Revisar logs: `docker-compose logs -f`
- Issues del proyecto: [GitHub Issues]

---

**¡Listo para extraer datos!** 🚀
