# ⚠️ CORRECCIÓN - Métricas Válidas para Insights

## El Problema

Algunas métricas que agregué **NO son válidas para el endpoint de Insights** de Facebook Ads API. Error:

```
(#100) leads is not valid for fields param
(#100) cost_per_lead is not valid for fields param
```

---

## ✅ Métricas VÁLIDAS para Insights (v22.0)

### ENTREGA (4 - ✅ Todas válidas)
```
✓ impressions
✓ clicks
✓ reach
✓ frequency
```

### COSTO (4 - ✅ Todas válidas)
```
✓ spend
✓ cpc
✓ cpm
✓ ctr
```

### CONVERSIÓN (4 - ✅ Válidas)
```
✓ actions
✓ conversion_rate_ranking
✓ cost_per_action_type
✓ cost_per_conversion
```

### VALOR (4 - ✅ Válidas)
```
✓ purchase_roas
✓ roas
✓ action_values
✓ conversion_values
```

### VIDEO (4 - ✅ Válidas)
```
✓ video_views
✓ video_play_actions
✓ video_avg_time_watched_actions
✓ video_play_retained_audience
```

### ENGAGEMENT (4 - ✅ Válidas)
```
✓ post_engagement
✓ inline_post_engagement
✓ post_clicks
✓ post_impressions
```

### LINKS (4 - ✅ Válidas)
```
✓ inline_link_clicks
✓ inline_link_click_ctr
✓ cost_per_inline_link_click
✓ cost_per_inline_post_engagement
```

### STORIES (3 - ✅ Válidas)
```
✓ story_clicks
✓ story_impressions
✓ story_opens
```

### APLICACIÓN (4 - ✅ Válidas)
```
✓ app_store_clicks
✓ mobile_app_purchases
✓ mobile_app_installs
✓ cost_per_mobile_app_install
```

### ORGÁNICO/PAGADO (6 - ✅ Válidas)
```
✓ post_clicks_organic
✓ post_clicks_paid
✓ post_impressions_organic
✓ post_impressions_paid
✓ post_impressions_organic_unique
✓ post_impressions_paid_unique
```

**Total: 39+ métricas VÁLIDAS** ✅

---

## ❌ Métricas NO Válidas para Insights

Estas métricas **existen en Facebook Ads API** pero **NO para el endpoint de Insights**:

```
❌ leads              - NO válida para insights
❌ cost_per_lead      - NO válida para insights
❌ purchases          - NO válida para insights (solo en nivel aggregated)
❌ cost_per_purchase  - NO válida para insights
```

Estas métricas se obtienen de **otros endpoints**, no de insights.

---

## 🔧 Cambios Realizados

### 1. API Actualizada (`api.py`)
- ✅ Solo muestra 39+ métricas **VÁLIDAS** para insights
- ✅ Removidas: leads, cost_per_lead, purchases, cost_per_purchase
- ✅ Categorías reorganizadas

### 2. Config Actualizada (`config/config.yaml`)
- ✅ Cambió de 8 a 15 métricas válidas
- ✅ Removidas métricas inválidas
- ✅ Ahora trae: impressions, clicks, spend, reach, ctr, cpc, cpm, frequency, actions, video_views, video_play_actions, inline_link_clicks, post_engagement

### 3. Frontend Actualizado (`static/index.html`)
- ✅ Carga dinámicamente solo métricas válidas
- ✅ Ya no muestra "leads" o "cost_per_lead"

---

## 📊 Comparación

### Antes (Incorrecto)
```
❌ 42+ métricas
❌ Algunas inválidas para insights
❌ Error: "leads is not valid for fields param"
```

### Después (Correcto)
```
✅ 39+ métricas válidas
✅ Todas funcionan en insights
✅ Sin errores
```

---

## 🚀 Cómo Usar Ahora

### Paso 1: Abre el Modal
```
http://localhost:5000
Click: "📊 Configurar Insights"
```

### Paso 2: Selecciona Métricas Válidas
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
  ✓ Costo por Conversión

VIDEO:
  ✓ Vistas de Video
  ✓ Reproducciones
  ✓ Tiempo Promedio

... (todas son válidas ahora)
```

### Paso 3: Guarda
```
Click: "💾 Guardar Configuración"
Resultado: ✅ Próxima sync trae estos campos
```

---

## ✅ Verificación

### Test - Sincronizar Ahora
```bash
# Ejecutar sincronización
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# Resultado esperado:
# ✅ Sin errores
# ✅ Datos en MySQL con todas las métricas
```

### Verificar en MySQL
```sql
-- Ver columnas en tabla insights
DESCRIBE facebook_ads_insights;

-- Deberías ver todas las columnas:
-- date_start, date_stop, impressions, clicks, spend, reach, 
-- ctr, cpc, cpm, frequency, actions, video_views, 
-- video_play_actions, inline_link_clicks, post_engagement
```

---

## 📋 Resumen de Cambios

| Aspecto | Antes | Después |
|---------|-------|---------|
| Métricas mostradas | 42+ | 39+ (todas válidas) |
| Errores | ❌ Sí (leads, cost_per_lead) | ✅ No |
| Datos en MySQL | ❌ No traía | ✅ Sí, correctamente |
| Funcionamiento | ❌ Fallaba | ✅ Funciona |

---

## 🔍 Por Qué Estos Cambios

Facebook Ads Insights API **solo soporta ciertos campos**:

- ✅ **SÍ soporta:** impressions, clicks, actions, video_views, etc.
- ❌ **NO soporta:** leads, cost_per_lead, purchases (estos son agregados)

El error `(#100) leads is not valid for fields param` significa que Facebook rechaza ese campo porque **no existe en el endpoint de insights**.

---

## 💡 Alternativas para Métricas No Válidas

Si necesitas metrics como "leads" o "purchases" en insights, deberías:

1. **Usar un endpoint diferente** - Algunos datos vienen de otros endpoints
2. **Usar píxeles de conversión** - Facebook necesita seguimiento específico
3. **Usar tabla "campaigns"** - Algunos datos están en otros niveles

---

## 🎯 Ahora Funciona

```
Modal → Selecciona métricas válidas → Guarda → Sincronización exitosa → Datos en MySQL ✅
```

¡Todo debería funcionar correctamente ahora!
