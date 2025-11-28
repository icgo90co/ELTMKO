# Sistema ELT - ELTMKO

Sistema de Extracción, Carga y Transformación (ELT) similar a Airbyte, diseñado para extraer datos de diversas plataformas y cargarlos en bases de datos MySQL.

## 🐳 Inicio Rápido con Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd ELTMKO

# 2. Configurar credenciales
cp .env.docker .env
nano .env  # Editar con tus credenciales de Facebook Ads

# 3. Verificar sistema (opcional)
./docker-verify.sh

# 4. Iniciar
./docker-start.sh

# 5. Abrir navegador
# http://localhost:5000
```

**¡Listo en 2 minutos!** ⚡

📖 **Más información**: [Guía Docker Completa](docs/DOCKER.md) | [Quick Start](DOCKER_QUICKSTART.md)

## 🚀 Características

- **Extracción de Datos**: Conectores para extraer datos de múltiples plataformas
  - ✅ Facebook Ads (campañas, ad sets, anuncios, insights)
  - 🔄 Fácil extensión para otras plataformas
- **Carga a MySQL**: Sistema robusto de carga de datos con soporte para upserts
- **Configuración Flexible**: Configuración basada en YAML para fuentes y destinos
- **Interfaz Web Completa**: Panel de control con:
  - 🎛️ Configuración de credenciales (Facebook Ads, MySQL)
  - 📊 Visualización de pipelines activos
  - 📋 Selección de tablas a sincronizar
  - 📈 Estadísticas de datos sincronizados
  - ▶️ Ejecución manual de pipelines
  - 🎯 **Selector dinámico de 50+ métricas de Facebook Ads API v22.0**
- **API REST**: Endpoints para integración programática
- **Ejecución Programada**: Sincronización automática con intervalos configurables
- **Logging Avanzado**: Sistema de logs con colores y múltiples niveles

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- Cuenta de Facebook Ads con acceso a la API

## 🛠️ Instalación

### Opción 1: Con Docker (Recomendado) 🐳

La forma más rápida de empezar. Docker se encarga de todo: base de datos, aplicación y dependencias.

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd ELTMKO

# 2. Configurar credenciales
cp .env.docker .env
# Editar .env con tus credenciales de Facebook Ads

# 3. Iniciar el sistema
./docker-start.sh
```

¡Listo! Abre http://localhost:5000 en tu navegador.

#### Comandos Docker útiles:

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Detener el sistema
./docker-stop.sh

# Ejecutar pipeline manualmente
./docker-run-pipeline.sh

# Iniciar con worker de sincronización automática
docker-compose --profile worker up -d
```

### Opción 2: Instalación Manual

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd ELTMKO
```

#### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_DATABASE=elt_data

# Facebook Ads Configuration
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
FACEBOOK_ACCESS_TOKEN=tu_access_token
FACEBOOK_AD_ACCOUNT_ID=act_tu_account_id

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
```

#### 5. Instalar y configurar MySQL

```bash
# Instalar MySQL (Ubuntu/Debian)
sudo apt-get install mysql-server

# Crear base de datos
mysql -u root -p
CREATE DATABASE elt_data;
```

#### 6. Configurar pipelines

Editar `config/config.yaml` para configurar tus fuentes y destinos:

```yaml
destinations:
  - name: "mysql_main"
    type: "mysql"
    enabled: true
    config:
      host: "${MYSQL_HOST}"
      port: ${MYSQL_PORT}
      user: "${MYSQL_USER}"
      password: "${MYSQL_PASSWORD}"
      database: "${MYSQL_DATABASE}"

sources:
  - name: "facebook_ads"
    type: "facebook_ads"
    enabled: true
    destination: "mysql_main"
    config:
      app_id: "${FACEBOOK_APP_ID}"
      app_secret: "${FACEBOOK_APP_SECRET}"
      access_token: "${FACEBOOK_ACCESS_TOKEN}"
      ad_account_id: "${FACEBOOK_AD_ACCOUNT_ID}"
    sync:
      interval_minutes: 60
      tables:
        - name: "campaigns"
          fields: ["id", "name", "status", "objective", "created_time"]
        - name: "insights"
          fields: ["date_start", "impressions", "clicks", "spend"]
          date_range: 30
```

## 🎯 Uso

### Con Docker 🐳

#### Opción 1: Interfaz Web (Recomendado)
```bash
./docker-start.sh
# Abrir http://localhost:5000
```

#### Opción 2: Ejecutar pipeline una vez
```bash
./docker-run-pipeline.sh
```

#### Opción 3: Worker con sincronización automática
```bash
docker-compose --profile worker up -d
```

### Sin Docker (Instalación Manual)

#### Modo 1: Ejecución única

Ejecutar todos los pipelines una vez:

```bash
python main.py --mode once
```

#### Modo 2: Ejecución programada

Ejecutar pipelines continuamente según intervalos configurados:

```bash
python main.py --mode scheduled
```

#### Modo 3: API Web con interfaz

Iniciar servidor web con panel de control:

```bash
python api.py
```

Luego abrir en el navegador: `http://localhost:5000`

## 🐳 Arquitectura Docker

El sistema utiliza 3 servicios en Docker:

1. **MySQL**: Base de datos para almacenar los datos extraídos
2. **ELT-API**: Servidor web con interfaz de control
3. **ELT-Worker**: (Opcional) Sincronización automática programada

```
┌─────────────┐      ┌──────────────┐      ┌────────────────┐
│             │      │              │      │                │
│   MySQL     │◄─────│   ELT-API    │◄─────│   Navegador    │
│  (Puerto    │      │  (Puerto     │      │  (localhost:   │
│   3306)     │      │   5000)      │      │    5000)       │
│             │      │              │      │                │
└─────────────┘      └──────────────┘      └────────────────┘
       ▲
       │
       │
┌──────┴──────┐
│             │
│ ELT-Worker  │
│ (Opcional)  │
│             │
└─────────────┘
```

### Volúmenes Docker

Los datos persisten en volúmenes Docker:
- `mysql_data`: Datos de la base de datos
- `./config`: Configuraciones
- `./logs`: Logs del sistema

## 🔧 Configuración Docker

### Variables de entorno

Editar `.env` para configurar:

```env
# MySQL
MYSQL_USER=eltuser
MYSQL_PASSWORD=eltpassword
MYSQL_DATABASE=elt_data

# Facebook Ads (requerido)
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
FACEBOOK_ACCESS_TOKEN=tu_token
FACEBOOK_AD_ACCOUNT_ID=act_tu_account

# API
API_PORT=5000
```

### Personalizar docker-compose.yml

Para cambiar puertos o configuraciones, editar `docker-compose.yml`:

```yaml
services:
  elt-api:
    ports:
      - "8080:5000"  # Cambiar puerto externo
```

## 🌐 API REST

### Endpoints disponibles

#### Salud del sistema
```bash
GET /health
```

#### Listar fuentes
```bash
GET /api/sources
```

#### Obtener fuente específica
```bash
GET /api/sources/{source_name}
```

#### Listar destinos
```bash
GET /api/destinations
```

#### Listar pipelines
```bash
GET /api/pipelines
```

#### Ejecutar todos los pipelines
```bash
POST /api/pipelines/run
```

#### Ejecutar pipeline específico
```bash
POST /api/pipelines/run/{source_name}
```

#### Recargar configuración
```bash
POST /api/config/reload
```

### Ejemplo de uso con curl

```bash
# Ejecutar pipeline de Facebook Ads
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# Listar todas las fuentes
curl http://localhost:5000/api/sources

# Ver tablas disponibles
curl http://localhost:5000/api/tables/available

# Ver estadísticas de datos
curl http://localhost:5000/api/data/stats

# Actualizar configuración de Facebook Ads
curl -X POST http://localhost:5000/api/sources/facebook_ads/config \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "tu_app_id",
    "app_secret": "tu_app_secret",
    "access_token": "tu_token",
    "ad_account_id": "act_123456"
  }'
```

## 🎛️ Configuración desde la Interfaz Web

La interfaz web (http://localhost:5000) permite configurar todo sin editar archivos:

### 1. Configurar Facebook Ads
- Click en "⚙️ Configurar" en la sección de Fuentes
- Ingresar credenciales:
  - App ID
  - App Secret
  - Access Token
  - Ad Account ID
- Activar/desactivar la fuente
- Guardar

### 2. Configurar MySQL
- Click en "⚙️ Configurar" en la sección de Destinos
- Configurar conexión:
  - Host (mysql para Docker)
  - Puerto (3306)
  - Usuario
  - Contraseña
  - Base de datos
- Guardar

### 3. Seleccionar Tablas a Sincronizar
- Ver sección "Tablas Disponibles"
- Activar/desactivar tablas con el toggle switch:
  - 📊 campaigns (campañas)
  - 📊 adsets (conjuntos de anuncios)
  - 📊 ads (anuncios)
  - 📊 insights (métricas)

### 4. Ver Datos Sincronizados
- Sección "Datos Sincronizados" muestra:
  - Número de registros por tabla
  - Última fecha de sincronización
  - Estado de cada tabla

## 📁 Estructura del Proyecto

```
ELTMKO/
├── config/
│   └── config.yaml          # Configuración de pipelines
├── src/
│   ├── core/
│   │   ├── config_manager.py    # Gestor de configuración
│   │   └── logger.py            # Sistema de logging
│   ├── extractors/
│   │   └── facebook_ads_extractor.py  # Extractor de Facebook Ads
│   └── loaders/
│       └── mysql_loader.py      # Cargador MySQL
├── static/
│   └── index.html           # Interfaz web
├── main.py                  # Punto de entrada principal
├── api.py                   # Servidor API REST
├── requirements.txt         # Dependencias Python
├── .env.example            # Plantilla de variables de entorno
└── README.md               # Este archivo
```

## 🔧 Agregar Nuevos Conectores

### 1. Crear extractor

Crear archivo en `src/extractors/tu_plataforma_extractor.py`:

```python
import pandas as pd

class TuPlataformaExtractor:
    def __init__(self, config):
        self.config = config
        # Inicializar cliente API
    
    def extract_table(self, table_config):
        # Lógica de extracción
        return pd.DataFrame(data)
```

### 2. Registrar en orquestador

Modificar `src/orchestrator.py`:

```python
def _create_extractor(self):
    if self.source_type == 'tu_plataforma':
        return TuPlataformaExtractor(self.source_config.get('config', {}))
    # ... resto del código
```

### 3. Configurar en config.yaml

```yaml
sources:
  - name: "mi_fuente"
    type: "tu_plataforma"
    enabled: true
    destination: "mysql_main"
    config:
      api_key: "${TU_API_KEY}"
```

## 📊 Tablas Creadas en MySQL

El sistema crea automáticamente las siguientes tablas:

- `facebook_ads_campaigns`: Campañas de Facebook Ads
- `facebook_ads_adsets`: Conjuntos de anuncios
- `facebook_ads_ads`: Anuncios individuales
- `facebook_ads_insights`: Métricas e insights

Todas las tablas incluyen columnas de metadatos:
- `_elt_loaded_at`: Timestamp de carga inicial
- `_elt_updated_at`: Timestamp de última actualización

## 🐛 Solución de Problemas

### Con Docker

#### El contenedor MySQL no inicia
```bash
# Ver logs de MySQL
docker-compose logs mysql

# Reiniciar contenedor
docker-compose restart mysql

# Eliminar y recrear volumen (⚠️ elimina datos)
docker-compose down -v
docker-compose up -d
```

#### Error "Cannot connect to MySQL"
```bash
# Verificar que MySQL esté saludable
docker-compose ps

# Esperar más tiempo para que MySQL inicie
docker-compose logs -f mysql
```

#### Cambiar puerto de la API
Editar `.env`:
```env
API_PORT=8080
```

#### Ver logs en tiempo real
```bash
# Todos los servicios
docker-compose logs -f

# Solo API
docker-compose logs -f elt-api

# Solo MySQL
docker-compose logs -f mysql
```

### Sin Docker

#### Error de conexión a MySQL

```bash
# Verificar que MySQL esté corriendo
mysql -u root -p

# Crear base de datos si no existe
CREATE DATABASE elt_data;
```

### Error de autenticación de Facebook

1. Verificar que el token de acceso sea válido
2. Comprobar permisos de la aplicación de Facebook
3. Regenerar token desde Facebook Developer Console

### Logs detallados

Los logs se guardan en `logs/elt.log`. Para más detalles, cambiar el nivel en `config/config.yaml`:

```yaml
logging:
  level: "DEBUG"  # Cambiado de INFO a DEBUG
```

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork del repositorio
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📧 Contacto

Para preguntas o soporte, abrir un issue en el repositorio.

---

**Hecho con ❤️ para simplificar la integración de datos**
