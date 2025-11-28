# 🚀 Cómo Ver Todas las Métricas de Facebook Ads API en el Modal

## ✅ Ya está implementado - Cambios realizados

He actualizado el sistema para que **TODAS las métricas disponibles de la API de Facebook Ads v22.0** aparezcan en el modal de configuración.

---

## 📊 Lo Nuevo

### Antes (8 métricas hardcodeadas)
```
✓ Impresiones
✓ Clics
✓ Gasto
✓ Alcance
✓ CTR
✓ CPC
✓ CPM
✓ Frecuencia
```

### Ahora (50+ métricas disponibles)
```
ENTREGA:
✓ Impresiones
✓ Clics
✓ Alcance
✓ Frecuencia

COSTO:
✓ Gasto
✓ CPC
✓ CPM
✓ CTR

CONVERSIÓN:
✓ Acciones
✓ Ranking de Conversión
✓ Costo por Acción

COMPRAS:
✓ ROAS (Compras)
✓ Compras
✓ Costo por Compra

LEADS:
✓ Leads
✓ Costo por Lead

ENGAGEMENT:
✓ Engagement Post
✓ Engagement Inline
✓ Clics en Stories
✓ Impresiones Stories
✓ Aperturas Stories

VIDEO:
✓ Vistas de Video
✓ Reproducciones Video
✓ Tiempo Promedio Video

LINKS:
✓ Clics en Enlace
✓ CTR Enlace
✓ Costo por Clic Enlace
✓ Costo por Engagement

ATRIBUCIÓN:
✓ Valor de Acciones
✓ Valor de Conversiones
✓ ROAS General
✓ Valor por Conversión

APLICACIÓN:
✓ Clics a Tienda
✓ Compras en App
✓ Instalaciones App
✓ Costo por Instalación

ORGÁNICO/PAGADO:
✓ Clics Orgánicos
✓ Clics Pagados
✓ Impresiones Orgánicas
✓ Impresiones Pagadas
✓ Alcance Orgánico Único
✓ Alcance Pagado Único
```

---

## 🔧 Cambios Técnicos Realizados

### 1. API Actualizada (`api.py`)
- **Endpoint:** `/api/insights/available-fields` (GET)
- **Cambio:** Ahora devuelve 50+ métricas en lugar de 8 hardcodeadas
- **Categorización:** Métricas agrupadas por categoría (Entrega, Costo, Conversión, etc.)
- **Información:** Cada métrica tiene label, category, description

```python
# Ejemplo de respuesta
{
  "success": true,
  "data": {
    "metrics": {
      "impressions": {
        "label": "Impresiones",
        "category": "Entrega",
        "description": "Número de veces que se mostró el anuncio"
      },
      "purchases": {
        "label": "Compras",
        "category": "Compras",
        "description": "Número de compras generadas"
      },
      // ... 50+ métricas más
    }
  }
}
```

### 2. Frontend Actualizado (`static/index.html`)
- **Cambio:** Modal ahora carga dinámicamente las métricas desde la API
- **Mejora:** Las métricas se agrupan por categoría automáticamente
- **Interfaz:** Grid de 2 columnas para fácil lectura
- **Scroll:** Contenedor con scroll si hay muchas métricas
- **Información:** Cada checkbox muestra la descripción al pasar el mouse

```javascript
// Nueva función que carga todas las métricas
loadAvailableMetrics() {
  // 1. Obtiene datos de /api/insights/available-fields
  // 2. Agrupa por categoría
  // 3. Genera HTML dinámicamente
  // 4. Mantiene selecciones previas
}
```

---

## 🎯 Cómo Usar

### Paso 1: Abre el Modal
```
Web: http://localhost:5000
Click: "📊 Configurar Insights"
```

### Paso 2: Ve TODAS las Métricas
```
En la sección "Métricas a Incluir"
Verás: Todas las opciones agrupadas por categoría
```

### Paso 3: Selecciona las Que Necesitas
```
Por ejemplo, para E-Commerce:
✓ impressions
✓ clicks
✓ spend
✓ purchases (← NUEVO)
✓ cost_per_purchase (← NUEVO)
✓ purchase_roas (← NUEVO)
```

### Paso 4: Guarda
```
Click: "💾 Guardar Configuración"
Resultado: ✅ Las próximas sincronizaciones usarán estas métricas
```

---

## 📋 Ejemplos por Caso de Uso

### E-Commerce / Tienda Online
**Objetivo:** Rastrear ventas y ROI

Selecciona:
```
ENTREGA:
✓ impressions
✓ clicks

COSTO:
✓ spend
✓ cpc
✓ cpm

COMPRAS:
✓ purchases (IMPORTANTE)
✓ cost_per_purchase (IMPORTANTE)
✓ purchase_roas (IMPORTANTE)

ATRIBUCIÓN:
✓ roas
```

### Generador de Leads
**Objetivo:** Optimizar conversión de leads

Selecciona:
```
ENTREGA:
✓ impressions
✓ clicks
✓ reach

COSTO:
✓ spend
✓ cpc

LEADS:
✓ leads (IMPORTANTE)
✓ cost_per_lead (IMPORTANTE)

CONVERSIÓN:
✓ actions
```

### Video Marketing
**Objetivo:** Maximizar visualizaciones de video

Selecciona:
```
ENTREGA:
✓ impressions
✓ clicks

COSTO:
✓ spend
✓ cpm

VIDEO:
✓ video_views (IMPORTANTE)
✓ video_play_actions (IMPORTANTE)
✓ video_avg_time_watched_actions (IMPORTANTE)
```

### App Store
**Objetivo:** Aumentar descargas de aplicación

Selecciona:
```
ENTREGA:
✓ impressions
✓ clicks

COSTO:
✓ spend
✓ cpc

APLICACIÓN:
✓ mobile_app_installs (IMPORTANTE)
✓ cost_per_mobile_app_install (IMPORTANTE)
```

### Engagement / Social
**Objetivo:** Maximizar interacciones

Selecciona:
```
ENTREGA:
✓ impressions
✓ reach
✓ frequency

ENGAGEMENT:
✓ post_engagement (IMPORTANTE)
✓ inline_post_engagement (IMPORTANTE)
✓ story_clicks (IMPORTANTE)

COSTO:
✓ spend
```

---

## 🔍 Cómo Verificar que Funciona

### Opción 1: Desde el Navegador
```
1. Abre http://localhost:5000
2. Click: "📊 Configurar Insights"
3. Desplázate en la sección "Métricas a Incluir"
4. Verás: Métricas agrupadas por categoría
5. Ej: COMPRAS, LEADS, VIDEO, etc.
```

### Opción 2: Desde la API
```bash
curl http://localhost:5000/api/insights/available-fields | jq '.data.metrics'
```

Output esperado:
```json
{
  "impressions": {
    "label": "Impresiones",
    "category": "Entrega",
    "description": "..."
  },
  "purchases": {
    "label": "Compras",
    "category": "Compras",
    "description": "..."
  },
  // ... 50+ métricas más
}
```

### Opción 3: Guarda una Configuración Personalizada
```bash
curl -X POST http://localhost:5000/api/insights/config \
  -H "Content-Type: application/json" \
  -d '{
    "level": "campaign",
    "time_increment": "daily",
    "date_range": 30,
    "fields": [
      "impressions",
      "clicks",
      "spend",
      "purchases",
      "purchase_roas",
      "cost_per_purchase",
      "leads",
      "video_views"
    ]
  }'
```

---

## 📝 Notas Importantes

⚠️ **No todas las métricas están disponibles para todos los tipos de campaña:**
- `purchases` - Solo si tienes píxel de conversión configurado
- `leads` - Solo si tienes formularios de leads
- `video_*` - Solo para campañas con video
- `app_*` - Solo para campañas de aplicación
- `story_*` - Solo para anuncios en Stories

✅ **Tip:** 
- Empieza con las 8 métricas básicas (impressions, clicks, spend, reach, ctr, cpc, cpm, frequency)
- Ve agregando más según necesites
- Puedes cambiar en cualquier momento

✅ **Disponibilidad:**
- Las métricas pueden no estar disponibles para fechas muy antiguas
- Facebook mantiene cambios en métricas por compatibilidad
- Consulta `AVAILABLE_METRICS.md` para lista completa

---

## 🎓 Documentación Relacionada

📄 **AVAILABLE_METRICS.md** - Lista completa con descripciones
📄 **INSIGHTS_CONFIGURATION_GUIDE.md** - Guía de configuración
📄 **TESTING_GUIDE.md** - Pruebas paso a paso
📄 **QUICK_REFERENCE.md** - Referencia rápida

---

## 🚀 Próximos Pasos

### Para el Usuario
1. Abre el modal (botón "📊 Configurar Insights")
2. Observa todas las métricas disponibles
3. Selecciona las que necesitas
4. Guarda la configuración
5. Ejecuta la sincronización

### Para el Desarrollador
- Las métricas se cargan dinámicamente de la API
- Fácil agregar nuevas métricas en el futuro
- Backend ya soporta cualquier métrica que devuelva Facebook API v22.0

---

## ❓ FAQ

**P:** ¿Por qué no veo todas las métricas?
**R:** Asegúrate de:
1. Recargar la página (Ctrl+Shift+R)
2. Verificar que el servidor API está corriendo
3. Abrir las herramientas de desarrollador (F12) para ver errores

**P:** ¿Puedo usar métricas que no aparecen en la lista?
**R:** Sí, puedes editarlas directamente en `config/config.yaml` bajo el campo `fields`.

**P:** ¿Qué métrica es mejor para X objetivo?
**R:** Lee la sección "Ejemplos por Caso de Uso" arriba, o consulta `AVAILABLE_METRICS.md`.

**P:** ¿Se guardan mis selecciones?
**R:** Sí, se guardan en `config/config.yaml` y se cargan cada vez que abres el modal.

---

✨ **¡Ya está listo para usar!** Abre el modal y explora todas las métricas disponibles.
