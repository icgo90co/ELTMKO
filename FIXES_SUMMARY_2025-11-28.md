# Resumen de Fixes - 28 de Noviembre 2025

## 🎯 Problemas Resueltos

### 1. ❌ Métricas Inválidas para Facebook Ads Insights
**Error:** `(#100) post_engagement, video_views are not valid for fields param`

**Causa:** Algunas métricas incluidas en la lista de disponibles no eran válidas para el endpoint `/insights` de Facebook Ads API.

**Solución:**
- ✅ Removidas métricas inválidas: `post_engagement`, `video_views`, `story_*`, `post_*`
- ✅ Removidas 15+ métricas no válidas de `/api/insights/available-fields`
- ✅ Actualizado `config.yaml` con solo métricas válidas
- ✅ Removido campo `creative` de la tabla `ads` (era objeto AdCreative sin conversión)

**Archivos modificados:** `api.py`, `config.yaml`, `src/extractors/facebook_ads_extractor.py`

---

### 2. ❌ Nuevas Columnas No Aparecían en MySQL
**Error:** Seleccionabas nuevas métricas pero no aparecían como columnas en la base de datos

**Causa:** El `MySQLLoader` solo creaba las tablas la primera vez. En sincronizaciones posteriores, no agregaba las nuevas columnas.

**Solución:**
- ✅ Agregado método `_add_missing_columns()` en `MySQLLoader`
- ✅ Detecta automáticamente columnas faltantes en tablas existentes
- ✅ Ejecuta `ALTER TABLE ... ADD COLUMN` para cada columna nueva
- ✅ Se llama automáticamente antes de cada upsert

**Archivos modificados:** `src/loaders/mysql_loader.py`

---

### 3. ❌ Rango de Fechas Ignorado
**Error:** Especificabas múltiples meses pero siempre se tomaban los últimos 30 días

**Causa:** Conflicto entre `date_range` (últimos N días) y `start_date`/`end_date` (fechas específicas). Ambos se guardaban juntos, causando ambigüedad.

**Solución:**
- ✅ Mejorada lógica en `index.html`: Si completás fechas específicas, NO envía `date_range`
- ✅ Mejorada lógica en `api.py`: Guarda SOLO uno de los dos métodos (nunca ambos)
- ✅ Si hay `start_date` + `end_date`: elimina `date_range` del config
- ✅ Si hay `date_range`: elimina `start_date` + `end_date` del config

**Archivos modificados:** `static/index.html`, `api.py`

---

### 4. ❌ Error "Python type list cannot be converted"
**Error:** `Failed executing the operation; Python type list cannot be converted`

**Causa:** Algunos campos de Facebook Ads API retornan estructuras complejas (listas de objetos) que MySQL no puede almacenar directamente:
- `actions` → `[{'action_type': 'link_click', 'value': '100'}, ...]`
- `action_values` → `[{'action_type': 'purchase', 'value': '1000'}, ...]`

**Solución:**
- ✅ Agregada lógica en `extract_insights()` para detectar campos complejos
- ✅ Convierte listas/diccionarios a strings JSON usando `json.dumps()`
- ✅ MySQL los almacena como TEXT con JSON válido
- ✅ Datos completos se preservan, solo cambia el formato

**Archivos modificados:** `src/extractors/facebook_ads_extractor.py`

---

## 📊 Resumen de Cambios

| Problema | Archivo | Cambios |
|----------|---------|---------|
| Métricas inválidas | `api.py` | Removidas 15+ métricas inválidas |
| Métricas inválidas | `config.yaml` | Removidos campos `post_engagement`, `video_views`, `creative` |
| Columnas faltantes | `mysql_loader.py` | +1 nuevo método `_add_missing_columns()` |
| Rango de fechas | `index.html` | Lógica mejorada de envío de fechas |
| Rango de fechas | `api.py` | Lógica mejorada de guardado en config |
| Campos complejos | `facebook_ads_extractor.py` | +Serialización JSON de listas/dicts |

---

## ✅ Verificación

Para confirmar que todo funciona correctamente:

### Test 1: Nuevas métricas
1. Abre modal "📊 Configurar Insights"
2. Selecciona nuevas métricas (ej: `actions`, `video_play_actions`)
3. Guarda configuración
4. Ejecuta sincronización
5. **Resultado esperado:** Nuevas columnas aparecen en MySQL

### Test 2: Rango de fechas
1. En el modal, especifica fechas exactas (ej: 01/07/2025 a 30/09/2025)
2. Ejecuta sincronización
3. **Resultado esperado:** Solo datos de ese rango aparecen en MySQL

### Test 3: Campos complejos
1. Si incluyes `actions` o `action_values` en las métricas
2. Ejecuta sincronización
3. **Resultado esperado:** Datos se guardan como JSON strings en MySQL (sin errores)

---

## 🔧 Archivos Modificados

1. **`api.py`**
   - Removidas métricas inválidas de `/api/insights/available-fields`
   - Mejorada lógica de guardado de fechas en `/api/insights/config` POST

2. **`config/config.yaml`**
   - Removidas métricas inválidas de la tabla `insights`
   - Removido campo `creative` de la tabla `ads`

3. **`src/loaders/mysql_loader.py`**
   - Agregado método `_add_missing_columns()`
   - Integrado en `upsert_dataframe()`

4. **`src/extractors/facebook_ads_extractor.py`**
   - Agregado `import json`
   - Agregada serialización de campos complejos en `extract_insights()`

5. **`static/index.html`**
   - Mejorada lógica de envío de configuración en el formulario

---

## 📌 Notas Importantes

- **Facebook Ads API v22.0** es estricto con validación de campos por endpoint
- Diferentes endpoints soportan diferentes campos
- El endpoint `/insights` es especialmente restrictivo
- Para futuros cambios, siempre valida métricas contra [documentación oficial de Facebook](https://developers.facebook.com/docs/marketing-api/reference/ads-insights/)

---

**Última actualización:** 2025-11-28 20:45
**Estado:** ✅ Todos los fixes implementados y listos para testing
