# Sistema ELT - ELTMKO

Sistema de Extracción, Carga y Transformación (ELT) similar a Airbyte, diseñado para extraer datos de diversas plataformas y cargarlos en bases de datos MySQL.

## 🚀 Características

- **Extracción de Datos**: Conectores para extraer datos de múltiples plataformas
  - ✅ Facebook Ads (campañas, ad sets, anuncios, insights)
  - 🔄 Fácil extensión para otras plataformas
- **Carga a MySQL**: Sistema robusto de carga de datos con soporte para upserts
- **Configuración Flexible**: Configuración basada en YAML para fuentes y destinos
- **Interfaz Web**: Panel de control para gestionar pipelines y ejecutar sincronizaciones
- **API REST**: Endpoints para integración programática
- **Ejecución Programada**: Sincronización automática con intervalos configurables
- **Logging Avanzado**: Sistema de logs con colores y múltiples niveles

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- Cuenta de Facebook Ads con acceso a la API

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd ELTMKO
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

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

### 5. Configurar pipelines

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

### Modo 1: Ejecución única

Ejecutar todos los pipelines una vez:

```bash
python main.py --mode once
```

### Modo 2: Ejecución programada

Ejecutar pipelines continuamente según intervalos configurados:

```bash
python main.py --mode scheduled
```

### Modo 3: API Web con interfaz

Iniciar servidor web con panel de control:

```bash
python api.py
```

Luego abrir en el navegador: `http://localhost:5000`

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
```

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

### Error de conexión a MySQL

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
