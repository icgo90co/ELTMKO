# 🚀 Guía de Despliegue en Producción

## Pre-requisitos

- Servidor con Docker y Docker Compose instalados
- Puertos 5000 y 3306 disponibles (o configurar otros)
- Credenciales de Facebook Ads válidas

## Despliegue Paso a Paso

### 1. Preparar el Servidor

```bash
# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker (si no está instalado)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

### 2. Clonar el Repositorio

```bash
# Clonar
git clone <repository-url> /opt/eltmko
cd /opt/eltmko

# Permisos para scripts
chmod +x docker-*.sh setup.sh
```

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.docker .env

# Editar con credenciales reales
nano .env
```

**Variables críticas a configurar**:
```env
# MySQL - Usar contraseñas fuertes en producción
MYSQL_PASSWORD=<contraseña-segura>

# Facebook Ads - Credenciales reales
FACEBOOK_APP_ID=<tu-app-id>
FACEBOOK_APP_SECRET=<tu-app-secret>
FACEBOOK_ACCESS_TOKEN=<tu-token>
FACEBOOK_AD_ACCOUNT_ID=act_<tu-account-id>

# API - Cambiar secret key
API_SECRET_KEY=<generar-clave-segura>
```

### 4. Configurar Firewall (Opcional)

```bash
# Permitir puerto 5000 (API)
sudo ufw allow 5000/tcp

# Bloquear puerto MySQL del exterior (recomendado)
# MySQL solo debe ser accesible desde localhost
sudo ufw deny 3306/tcp
```

### 5. Iniciar el Sistema

```bash
# Opción 1: Script automatizado
./docker-start.sh

# Opción 2: Make
make install

# Opción 3: Docker Compose directo
docker-compose build
docker-compose up -d
```

### 6. Verificar Despliegue

```bash
# Ver estado de contenedores
docker-compose ps

# Verificar logs
docker-compose logs --tail=50

# Verificar conectividad
curl http://localhost:5000/health

# Verificar MySQL
docker-compose exec mysql mysql -u eltuser -p -e "SELECT 1"
```

## Configuración de Systemd (Inicio Automático)

Crear servicio systemd para inicio automático:

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/eltmko.service
```

Contenido del archivo:

```ini
[Unit]
Description=ELT System ELTMKO
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/eltmko
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Habilitar y iniciar el servicio:

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar inicio automático
sudo systemctl enable eltmko

# Iniciar servicio
sudo systemctl start eltmko

# Ver estado
sudo systemctl status eltmko
```

## Configuración de Nginx (Reverse Proxy)

### Instalar Nginx

```bash
sudo apt-get install nginx -y
```

### Configurar Virtual Host

```bash
sudo nano /etc/nginx/sites-available/eltmko
```

Contenido:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilitar sitio:

```bash
sudo ln -s /etc/nginx/sites-available/eltmko /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL con Let's Encrypt

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Auto-renovación (ya configurada por certbot)
sudo certbot renew --dry-run
```

## Worker de Sincronización Automática

Para habilitar sincronización continua:

```bash
# Iniciar worker
docker-compose --profile worker up -d

# Verificar
docker-compose ps

# Ver logs del worker
docker-compose logs -f elt-worker
```

## Monitoreo y Logs

### Ver Logs

```bash
# Logs en tiempo real
docker-compose logs -f

# Logs de las últimas 24 horas
docker-compose logs --since 24h

# Guardar logs a archivo
docker-compose logs > logs_$(date +%Y%m%d).txt
```

### Rotación de Logs

Configurar logrotate:

```bash
sudo nano /etc/logrotate.d/eltmko
```

Contenido:

```
/opt/eltmko/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
```

## Backups Automáticos

### Crear Script de Backup

```bash
nano /opt/eltmko/backup.sh
```

Contenido:

```bash
#!/bin/bash
BACKUP_DIR="/opt/eltmko/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup de MySQL
docker-compose -f /opt/eltmko/docker-compose.yml exec -T mysql \
  mysqldump -u eltuser -peltpassword elt_data > $BACKUP_DIR/mysql_$DATE.sql

# Backup de configuración
tar -czf $BACKUP_DIR/config_$DATE.tar.gz -C /opt/eltmko config/

# Limpiar backups antiguos (más de 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completado: $DATE"
```

Hacer ejecutable:

```bash
chmod +x /opt/eltmko/backup.sh
```

### Programar con Cron

```bash
crontab -e
```

Agregar:

```cron
# Backup diario a las 2 AM
0 2 * * * /opt/eltmko/backup.sh >> /opt/eltmko/logs/backup.log 2>&1
```

## Actualización del Sistema

```bash
cd /opt/eltmko

# Hacer backup antes
./backup.sh

# Obtener últimos cambios
git pull

# Reconstruir imágenes
docker-compose build --no-cache

# Reiniciar servicios
docker-compose down
docker-compose up -d

# Verificar
docker-compose ps
docker-compose logs --tail=50
```

## Monitoreo con Docker Stats

```bash
# Ver uso de recursos en tiempo real
docker stats

# O crear script de monitoreo
echo '#!/bin/bash
while true; do
    clear
    echo "=== ELT System Status ==="
    date
    echo ""
    docker-compose ps
    echo ""
    docker stats --no-stream
    sleep 5
done' > monitor.sh

chmod +x monitor.sh
./monitor.sh
```

## Seguridad

### 1. Firewall
```bash
# Permitir solo puertos necesarios
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable
```

### 2. Contraseñas Fuertes
- Cambiar contraseña de MySQL
- Cambiar API_SECRET_KEY
- Usar tokens de Facebook con permisos mínimos necesarios

### 3. Actualizaciones
```bash
# Actualizar regularmente
sudo apt-get update && sudo apt-get upgrade -y
docker-compose pull
docker-compose up -d
```

### 4. Limitar Acceso
- Usar Nginx con autenticación básica
- Implementar rate limiting
- Usar VPN para acceso administrativo

## Troubleshooting en Producción

### Sistema no inicia
```bash
# Ver logs
docker-compose logs

# Verificar Docker
sudo systemctl status docker

# Reiniciar Docker
sudo systemctl restart docker
```

### Alto uso de recursos
```bash
# Ver consumo
docker stats

# Limitar recursos en docker-compose.yml
services:
  elt-api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Base de datos llena
```bash
# Ver tamaño
docker-compose exec mysql mysql -u eltuser -p -e "
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES 
WHERE table_schema = 'elt_data'
ORDER BY (data_length + index_length) DESC;
"

# Limpiar datos antiguos si es necesario
```

## Checklist de Despliegue

- [ ] Docker y Docker Compose instalados
- [ ] Repositorio clonado
- [ ] Variables de entorno configuradas
- [ ] Firewall configurado
- [ ] Sistema iniciado y verificado
- [ ] Nginx configurado (si se usa)
- [ ] SSL configurado (si se usa)
- [ ] Systemd configurado para inicio automático
- [ ] Backups automáticos configurados
- [ ] Monitoreo configurado
- [ ] Documentación revisada

## Soporte

Para problemas en producción:
1. Revisar logs: `docker-compose logs`
2. Verificar estado: `docker-compose ps`
3. Consultar documentación: `docs/DOCKER.md`
4. Abrir issue en GitHub

---

**¡Sistema listo para producción!** 🚀
