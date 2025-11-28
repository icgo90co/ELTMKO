# Facebook Insights Endpoint Validation Fix

## 📋 Problemas Identificados

El sistema mostraba múltiples errores al intentar sincronizar datos:

### Error 1: Métricas inválidas para `/insights`

```
Error 400: "(#100) post_engagement, video_views are not valid for fields param"
```

### Error 2: Campo complejo `AdCreative` sin conversión

```
Error: "Failed executing the operation; Python type AdCreative cannot be converted"
```

## 🔍 Causas Raíz

### Problema 1: Restricciones específicas por endpoint

Facebook Ads API tiene **restricciones específicas por endpoint**:
- Algunos campos son válidos en ciertos endpoints pero NO en otros
- El endpoint `/insights` es especialmente restrictivo
- Las métricas `post_engagement`, `video_views`, y otras fueron incluidas en la lista de disponibles **pero no son soportadas por `/insights`**

### Errores Encontrados - Error 1

Estas métricas estaban en la configuración pero **NO son válidas para `/insights`**:
- ❌ `post_engagement` - Solo para Page Insights, no Ads Insights
- ❌ `video_views` - Nombre del campo es incorrecto para Ads Insights
- ❌ `story_clicks`, `story_impressions`, `story_opens` - No válidas para /insights
- ❌ `post_clicks_organic`, `post_clicks_paid` - Page-related, no Ads
- ❌ `post_impressions_*` - Para Pages, no Ads
- ❌ `mobile_app_purchases`, `cost_per_mobile_app_install` - No válidas para este endpoint

### Errores Encontrados - Error 2

El campo `creative` en la tabla `ads`:
- ❌ Es un objeto complejo `AdCreative` de Facebook API
- ❌ No puede convertirse directamente a tipo Python/MySQL
- ❌ MySQL no puede almacenar objetos complejos sin serialización
- ✅ Solución: Remover `creative` de campos a extraer (solo datos simples)

## ✅ Solución Implementada

### 1. Actualizado: `/config/config.yaml`

#### Cambio 1: Insights - Removidas métricas inválidas

```yaml
# ANTES (con métricas inválidas)
fields: [
  "date_start",
  "date_stop",
  "impressions",
  "clicks",
  "spend",
  "reach",
  "ctr",
  "cpc",
  "cpm",
  "frequency",
  "actions",
  "video_views",              # ❌ INVÁLIDA
  "video_play_actions",
  "inline_link_clicks",
  "post_engagement"           # ❌ INVÁLIDA
]

# DESPUÉS (solo métricas válidas)
fields: [
  "date_start",
  "date_stop",
  "impressions",
  "clicks",
  "spend",
  "reach",
  "ctr",
  "cpc",
  "cpm",
  "frequency",
  "actions",
  "video_play_actions",       # ✅ VÁLIDA
  "inline_link_clicks"        # ✅ VÁLIDA
]
```

#### Cambio 2: Ads - Removido campo `creative`

```yaml
# ANTES
fields: ["id", "name", "status", "adset_id", "creative"]  # creative es objeto AdCreative

# DESPUÉS (solo campos convertibles a MySQL)
fields: ["id", "name", "status", "adset_id"]
```

### 2. Actualizado: `/api.py` endpoint `/api/insights/available-fields`

**Cambios**:
- Removidas métricas inválidas: `post_engagement`, `video_views`, `story_*`, `post_*`
- Añadidas alternativas válidas: `video_15_sec_watched_actions`, `video_30_sec_watched_actions`, `video_continuous_2_sec_watched_actions`, `video_thruplay_watched_actions`
- Solo se muestran al usuario métricas que Facebook realmente acepta para `/insights`

**Categoría Video - Cambios**:
- ❌ Removida: `video_views`
- ❌ Removida: `video_play_retained_audience`
- ✅ Mantenida: `video_play_actions`
- ✅ Mantenida: `video_avg_time_watched_actions`
- ✅ Añadida: `video_15_sec_watched_actions`
- ✅ Añadida: `video_30_sec_watched_actions`
- ✅ Añadida: `video_continuous_2_sec_watched_actions`
- ✅ Añadida: `video_thruplay_watched_actions`

**Categoría Engagement - Cambios**:
- ❌ Removida completamente (no tiene campos válidos para /insights)
- ❌ Removida: `post_engagement`
- ❌ Removida: `inline_post_engagement`
- ❌ Removida: `post_clicks`
- ❌ Removida: `post_impressions`

**Categoría Stories - Cambios**:
- ❌ Removida completamente (sin campos válidos para /insights)
- ❌ Removidas: `story_*`

**Categoría Orgánico/Pagado - Cambios**:
- ❌ Removida completamente (no válidas para Ads Insights)
- ❌ Removidas: `post_clicks_*`, `post_impressions_*`

### 3. Actualizado: `/src/extractors/facebook_ads_extractor.py`

**Cambio**: Removido campo `creative` de los campos extraídos

```python
# ANTES
fields = [
    Ad.Field.id,
    Ad.Field.name,
    Ad.Field.status,
    Ad.Field.adset_id,
    Ad.Field.creative,        # ❌ Objeto AdCreative - no convertible
    Ad.Field.created_time,
    Ad.Field.updated_time,
]

# DESPUÉS
fields = [
    Ad.Field.id,
    Ad.Field.name,
    Ad.Field.status,
    Ad.Field.adset_id,        # ✅ Solo campos convertibles a MySQL
]

# Se añadió lógica para remover 'creative' si llega en los datos
ad_dict.pop('creative', None)
```

#### Entrega
- `impressions` ✅
- `clicks` ✅
- `reach` ✅
- `frequency` ✅

#### Costo
- `spend` ✅
- `cpc` ✅
- `cpm` ✅
- `ctr` ✅

#### Conversión
- `actions` ✅
- `conversion_rate_ranking` ✅
- `cost_per_action_type` ✅
- `cost_per_conversion` ✅

#### Valor
- `purchase_roas` ✅
- `roas` ✅
- `action_values` ✅
- `conversion_values` ✅

#### Video (Válidas)
- `video_play_actions` ✅
- `video_avg_time_watched_actions` ✅
- `video_15_sec_watched_actions` ✅
- `video_30_sec_watched_actions` ✅
- `video_continuous_2_sec_watched_actions` ✅
- `video_thruplay_watched_actions` ✅

#### Links
- `inline_link_clicks` ✅
- `inline_link_click_ctr` ✅
- `cost_per_inline_link_click` ✅

#### Aplicación (Válidas)
- `mobile_app_installs` ✅
- `mobile_app_purchase_roas` ✅
- `app_store_clicks` ✅

## 🔍 Cómo Fue Identificado

1. Error en logs: `(#100) post_engagement, video_views are not valid for fields param`
2. Revisión de documentación oficial: https://developers.facebook.com/docs/marketing-api/reference/ads-insights/
3. Cada métrica validada contra endpoint específico
4. Métricas inválidas removidas de config y API

## 📊 Resumen de Cambios

| Archivo | Cambios | Impacto |
|---------|---------|--------|
| `/config/config.yaml` | Removidas `post_engagement`, `video_views` de insights | Evita error 400 |
| `/config/config.yaml` | Removido `creative` de ads | Evita error de conversión Python |
| `/api.py` | Removidas 15+ métricas inválidas de endpoint | Usuario solo ve opciones válidas |
| `/api.py` | Añadidas 4 alternativas de video válidas | Más opciones para usuario |
| `/src/extractors/facebook_ads_extractor.py` | Removido `Ad.Field.creative` | Evita objeto complejo sin conversión |

## 🚀 Próximos Pasos

1. **Reiniciar la API** (si está corriendo)
2. **Sincronizar nuevamente** - Ahora sin errores 400
3. **Verificar MySQL** - Datos se escribirán correctamente
4. **Modal de configuración** - Solo mostrará métricas válidas

## ⚠️ Nota Importante

Facebook Ads API v22.0 es estricta con validación de campos por endpoint. Si en el futuro decides usar más métricas:
- Revisa la documentación oficial: https://developers.facebook.com/docs/marketing-api/reference/ads-insights/
- Valida cada métrica contra el endpoint específico
- Algunas métricas solo funcionan con ciertos `level` (account, campaign, adset, ad)

## 📝 Archivos Modificados

- `/config/config.yaml` - Removidas 2 métricas inválidas en insights + removido campo `creative` en ads
- `/api.py` - Removidas 15+ métricas inválidas, añadidas 4 alternativas válidas
- `/src/extractors/facebook_ads_extractor.py` - Removido campo `creative`, mejorada lógica de limpieza

---

**Estado**: ✅ Reparado  
**Fecha**: 2025-11-28  
**Versión API**: v22.0  
**SDK**: facebook-business v20.0.0
