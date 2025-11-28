# ✨ Cambios Realizados - Configuración Dinámica de Insights

Fecha: 28 de Noviembre, 2025

## Resumen

Se ha implementado un sistema completo para configurar dinámicamente:
- **Dimensiones** (Level): account, campaign, adset, ad
- **Métricas**: selección flexible de qué datos traer
- **Período de tiempo**: fechas exactas o últimos X días
- **Granularidad temporal**: diario o mensual

## Cambios en el Código

### 1. `src/extractors/facebook_ads_extractor.py`

#### Función `extract_insights()` mejorada:

**Antes:**
```python
def extract_insights(
    self,
    level: str = 'account',
    date_range: int = 30,
    fields: List[str] = None
) -> pd.DataFrame:
    # Solo soportaba date_range fijo
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=date_range)
    params = {
        'time_increment': 1,  # Siempre diario
    }
```

**Después:**
```python
def extract_insights(
    self,
    level: str = 'account',
    date_range: int = None,
    start_date: str = None,
    end_date: str = None,
    time_increment: str = 'daily',
    fields: List[str] = None
) -> pd.DataFrame:
    # Soporta fechas exactas, date_range, y granularidad configurable
    # time_increment: 'daily' (1) o 'monthly' (all_days)
```

**Nuevos parámetros:**
- `start_date`: Fecha inicio exacta (YYYY-MM-DD)
- `end_date`: Fecha fin exacta (YYYY-MM-DD)
- `time_increment`: 'daily' o 'monthly'

#### Método `extract_table()` mejorado:

Ahora pasa todos los parámetros de configuración al `extract_insights()`.

### 2. `api.py` - Nuevos Endpoints

#### GET `/api/insights/config`
```
Obtiene la configuración actual de insights
Respuesta: {
  "level": "account",
  "date_range": 30,
  "start_date": null,
  "end_date": null,
  "time_increment": "daily",
  "fields": ["impressions", "clicks", ...]
}
```

#### POST `/api/insights/config`
```
Actualiza la configuración de insights
Cuerpo: {
  "level": "campaign",
  "time_increment": "daily",
  "date_range": 30,
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "fields": ["impressions", "clicks", "spend"]
}
```

Esto actualiza `config/config.yaml` y recarga la configuración automáticamente.

#### GET `/api/insights/available-fields`
```
Retorna los campos y opciones disponibles
Respuesta incluye:
- Dimensiones (account, campaign, adset, ad)
- Métricas disponibles
- Incrementos de tiempo
```

### 3. `static/index.html` - Nueva UI

#### Nuevo Botón
```
"📊 Configurar Insights" en la sección de Tablas
```

#### Nuevo Modal
**Modal ID**: `insightsModal`

Contiene:
- Selector de dimensión (account/campaign/adset/ad)
- Selector de granularidad (daily/monthly)
- Campos de fecha (inicio/fin)
- Campo para "últimos X días"
- Checkboxes para seleccionar métricas
- Botones guardar/cancelar

#### Nuevas Funciones JavaScript
- `openInsightsModal()` - Abre el modal
- `closeInsightsModal()` - Cierra el modal
- `loadCurrentInsightsConfig()` - Carga la configuración actual
- Manejador de submit del formulario

### 4. `config/config.yaml` - Nueva Estructura

**Antes:**
```yaml
- name: "insights"
  fields: [...]
  date_range: 30
```

**Después:**
```yaml
- name: "insights"
  fields: [...]
  level: "account"
  date_range: 30
  time_increment: "daily"
  start_date: null
  end_date: null
```

## Flujo de Funcionamiento

```
Usuario abre modal
    ↓
Carga configuración actual (GET /api/insights/config)
    ↓
Usuario modifica valores
    ↓
Click "Guardar Configuración"
    ↓
POST a /api/insights/config con nuevos valores
    ↓
API actualiza config.yaml
    ↓
API recarga configuración
    ↓
Próxima ejecución usa nuevos parámetros
```

## Ejemplos de Uso

### Ejemplo 1: Cambiar a nivel de campaña

```javascript
fetch('http://localhost:5000/api/insights/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    level: 'campaign',
    time_increment: 'daily',
    date_range: 30,
    fields: ['impressions', 'clicks', 'spend']
  })
})
```

### Ejemplo 2: Traer datos de rango específico

```javascript
{
  level: 'adset',
  time_increment: 'daily',
  start_date: '2025-10-01',
  end_date: '2025-10-31',
  fields: ['clicks', 'spend', 'ctr', 'cpc']
}
```

### Ejemplo 3: Datos mensuales de toda la cuenta

```javascript
{
  level: 'account',
  time_increment: 'monthly',
  date_range: 365,
  fields: ['impressions', 'clicks', 'spend', 'reach', 'cpm']
}
```

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `src/extractors/facebook_ads_extractor.py` | +parámetros en `extract_insights()` |
| `api.py` | +3 nuevos endpoints |
| `static/index.html` | +1 modal nuevo, +4 funciones JS |
| `config/config.yaml` | +nuevos campos opcionales |

## Archivos Creados

| Archivo | Descripción |
|---------|------------|
| `INSIGHTS_CONFIGURATION_GUIDE.md` | Guía completa de configuración |
| `INSIGHTS_CHANGES_SUMMARY.md` | Este archivo |

## Compatibilidad Hacia Atrás

✅ **Totalmente compatible**

- Configuraciones antiguas siguen funcionando
- Valores por defecto mantienen comportamiento anterior
- No hay cambios en tablas de base de datos

## Próximos Pasos (Opcional)

Si en el futuro quieres extender esto:

1. **Presets**: Agregar configuraciones guardadas (ej: "Análisis Semanal")
2. **Histórico**: Guardar historial de cambios de configuración
3. **Validación**: Advertencias si configuración puede causar muchos datos
4. **Exportación**: Exportar config como JSON/YAML

---

**Desarrollado por**: GitHub Copilot
**Licencia**: MIT
