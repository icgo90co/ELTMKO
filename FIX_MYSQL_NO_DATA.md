# 🔄 Datos No Llegan a MySQL - Solución

## 🎯 El Problema

Las métricas que seleccionaste en el modal se guardan en `config/config.yaml`, **PERO** si el config.yaml tiene métricas antiguas hardcodeadas, esas son las que se sincronizan.

**Solución:** Actualizar el `config.yaml` con las nuevas métricas que deseas.

---

## ✅ Solución - 3 Formas

### Forma 1: Automática (Recomendado) - Desde el Modal

```
1. Abre: http://localhost:5000
2. Click: "📊 Configurar Insights"
3. Selecciona las métricas que quieras
4. Configuración: Ej: 
   - Dimensión: campaign
   - Granularidad: daily
   - Período: 30 días
   - Métricas: selecciona las que necesites
5. Click: "💾 Guardar Configuración"
6. Verás: ✅ Confirmación
7. Siguiente sincronización usará ESTAS métricas
```

### Forma 2: Manual en el Archivo

Edita `/workspaces/ELTMKO/config/config.yaml`:

**Antes (8 métricas):**
```yaml
- name: "insights"
  fields: ["date_start", "date_stop", "impressions", "clicks", "spend", "reach", "ctr", "cpc", "cpm"]
  date_range: 30
```

**Después (con nuevas métricas):**
```yaml
- name: "insights"
  level: "campaign"                    # ← Agregado: nivel de agregación
  time_increment: "daily"              # ← Agregado: granularidad
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
    "actions",                         # ← NUEVO: Conversiones
    "purchases",                       # ← NUEVO: Compras
    "cost_per_purchase",               # ← NUEVO: Costo por compra
    "purchase_roas",                   # ← NUEVO: ROAS de compras
    "leads",                           # ← NUEVO: Leads
    "cost_per_lead",                   # ← NUEVO: Costo por lead
    "post_engagement",                 # ← NUEVO: Engagement en post
    "video_views",                     # ← NUEVO: Vistas de video
    "video_play_actions",              # ← NUEVO: Reproducciones video
    "video_avg_time_watched_actions"   # ← NUEVO: Tiempo video
  ]
  date_range: 30
```

### Forma 3: Por API (Programática)

```bash
curl -X POST http://localhost:5000/api/insights/config \
  -H "Content-Type: application/json" \
  -d '{
    "level": "campaign",
    "time_increment": "daily",
    "date_range": 30,
    "fields": [
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
      "purchases",
      "cost_per_purchase",
      "purchase_roas",
      "leads",
      "cost_per_lead",
      "post_engagement",
      "video_views"
    ]
  }'
```

---

## 🚀 Después de Actualizar

### Paso 1: Verifica que se Guardó
```bash
# Abre el archivo y verifica
cat /workspaces/ELTMKO/config/config.yaml | grep -A 20 "insights"
```

### Paso 2: Ejecuta la Sincronización
```bash
# Opción A: Desde el navegador
http://localhost:5000
→ Click: "▶️ Ejecutar Todos"

# Opción B: Por API
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# Opción C: Por terminal
python main.py --mode once
```

### Paso 3: Verifica MySQL
```bash
# Ver columnas de la tabla
mysql -h mysql -u eltuser -peltpassword elt_data -e "DESC facebook_ads_insights;"

# Ver datos con nuevas columnas
mysql -h mysql -u eltuser -peltpassword elt_data -e "SELECT * FROM facebook_ads_insights LIMIT 1;"

# Contar registros
mysql -h mysql -u eltuser -peltpassword elt_data -e "SELECT COUNT(*) FROM facebook_ads_insights;"
```

---

## 📊 Ejemplos de Configuración por Caso de Uso

### E-Commerce (Tienda Online)
```yaml
- name: "insights"
  level: "campaign"
  time_increment: "daily"
  fields: [
    "date_start",
    "date_stop",
    "campaign_id",
    "campaign_name",
    "impressions",
    "clicks",
    "spend",
    "reach",
    "frequency",
    "purchases",           # ← IMPORTANTE
    "cost_per_purchase",   # ← IMPORTANTE
    "purchase_roas",       # ← IMPORTANTE
    "cpc",
    "cpm",
    "ctr"
  ]
  date_range: 30
```

**Resultado en MySQL:**
```
┌─────────────┬──────────────────┬─────────────┬───────┬────────┬──────────────┬──────────────┬────────────────┐
│ date_start  │ campaign_name    │ impressions │ clicks│ spend  │ purchases    │ cost_per_purchase │ purchase_roas  │
├─────────────┼──────────────────┼─────────────┼───────┼────────┼──────────────┼──────────────┼────────────────┤
│ 2025-11-27  │ Campaign A       │ 10000       │ 500   │ $100   │ 50           │ $2.00        │ 5.0            │
│ 2025-11-27  │ Campaign B       │ 8000        │ 400   │ $80    │ 35           │ $2.29        │ 4.4            │
│ 2025-11-28  │ Campaign A       │ 12000       │ 600   │ $120   │ 60           │ $2.00        │ 5.0            │
└─────────────┴──────────────────┴─────────────┴───────┴────────┴──────────────┴──────────────┴────────────────┘
```

### Generador de Leads
```yaml
- name: "insights"
  level: "campaign"
  time_increment: "daily"
  fields: [
    "date_start",
    "date_stop",
    "campaign_id",
    "campaign_name",
    "impressions",
    "clicks",
    "spend",
    "leads",               # ← IMPORTANTE
    "cost_per_lead",       # ← IMPORTANTE
    "cpc",
    "cpm",
    "ctr"
  ]
  date_range: 30
```

### Video Marketing
```yaml
- name: "insights"
  level: "ad"
  time_increment: "daily"
  fields: [
    "date_start",
    "date_stop",
    "ad_id",
    "ad_name",
    "campaign_id",
    "impressions",
    "clicks",
    "spend",
    "video_views",              # ← IMPORTANTE
    "video_play_actions",       # ← IMPORTANTE
    "video_avg_time_watched_actions",  # ← IMPORTANTE
    "cpm"
  ]
  date_range: 30
```

### Todas las Métricas Disponibles
```yaml
- name: "insights"
  level: "campaign"
  time_increment: "daily"
  fields: [
    # Fechas
    "date_start",
    "date_stop",
    # IDs y Nombres
    "campaign_id",
    "campaign_name",
    # Entrega
    "impressions",
    "clicks",
    "reach",
    "frequency",
    # Costo
    "spend",
    "cpc",
    "cpm",
    "ctr",
    # Conversión
    "actions",
    "conversion_rate_ranking",
    # Compras
    "purchases",
    "cost_per_purchase",
    "purchase_roas",
    # Leads
    "leads",
    "cost_per_lead",
    # Engagement
    "post_engagement",
    "inline_post_engagement",
    # Video
    "video_views",
    "video_play_actions",
    "video_avg_time_watched_actions",
    # Links
    "inline_link_clicks",
    "inline_link_click_ctr",
    # Atribución
    "roas",
    "action_values"
  ]
  date_range: 30
```

---

## 🔍 Verificación Step-by-Step

### Paso 1: Verificar que se Guardó en config.yaml
```bash
cat /workspaces/ELTMKO/config/config.yaml | grep -A 30 "insights"
```

Expected output:
```yaml
- name: "insights"
  level: "campaign"
  time_increment: "daily"
  fields:
  - date_start
  - date_stop
  - impressions
  - clicks
  - spend
  - purchases
  ...
```

### Paso 2: Ejecutar Sincronización
```bash
# Opción A: Por navegador
Abre: http://localhost:5000
Click: "▶️ Ejecutar Todos"
Espera a que termine

# Opción B: Por terminal
docker exec eltmko-elt-api python main.py --mode once
```

### Paso 3: Ver Logs
```bash
# Ver logs en tiempo real
docker logs -f eltmko-elt-api

# O
tail -f /workspaces/ELTMKO/logs/elt.log
```

Espera a ver:
```
INFO - Extracting insights from Facebook Ads (level=campaign, dates=..., granularity=daily)
INFO - Loaded X rows into facebook_ads_insights
```

### Paso 4: Verificar MySQL
```bash
# Ver estructura de la tabla
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "DESCRIBE facebook_ads_insights;"

# Ver primeros registros
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SELECT * FROM facebook_ads_insights LIMIT 5;"

# Ver columnas disponibles
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SHOW COLUMNS FROM facebook_ads_insights;"
```

---

## ❓ Troubleshooting

### P: Actualicé config.yaml pero MySQL sigue sin nuevas columnas
**R:** Necesitas hacer **2 cosas**:
1. Editar `config/config.yaml`
2. Ejecutar la sincronización (click "▶️ Ejecutar Todos" o `python main.py`)

### P: Las tablas MySQL existentes no se actualizan automáticamente
**R:** El sistema agrega nuevas columnas cuando sincroniza. Si las columnas ya existen, verifica:
```bash
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SELECT COUNT(purchases) FROM facebook_ads_insights LIMIT 1;"
```

### P: ¿Cómo borro las tablas y empiezo desde cero?
**R:** Conecta a MySQL y ejecuta:
```bash
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "DROP TABLE IF EXISTS facebook_ads_insights;"

# Luego ejecuta sincronización
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads
```

### P: No veo los cambios reflejados
**R:** Intenta:
1. Recarga el navegador (Ctrl+Shift+R)
2. Espera 1-2 minutos a la siguiente sincronización
3. Verifica que el config.yaml se guardó correctamente
4. Mira los logs: `docker logs -f eltmko-elt-api`

---

## ✅ Checklist de Verificación

- [ ] Actualicé `config/config.yaml` con las nuevas métricas
- [ ] Ejecuté la sincronización (botón "▶️ Ejecutar Todos")
- [ ] Espéré a que terminara (ver confirmación en pantalla)
- [ ] Conté registros en MySQL: `SELECT COUNT(*) FROM facebook_ads_insights;`
- [ ] Verifiqué que las nuevas columnas existen: `DESCRIBE facebook_ads_insights;`
- [ ] Verifiqué que hay datos: `SELECT * FROM facebook_ads_insights LIMIT 1;`

---

## 🎯 Próximos Pasos

1. **Ahora:** Actualiza `config.yaml` con las métricas que necesitas
2. **Luego:** Ejecuta sincronización
3. **Verifica:** Revisa MySQL que traiga los datos
4. **Analiza:** Los datos están listos para análisis

---

## 📚 Documentación Relacionada

- `AVAILABLE_METRICS.md` - Lista completa de métricas disponibles
- `QUICK_METRICS_START.md` - Guía de 2 minutos
- `ALL_METRICS_VISIBLE.md` - Guía completa del modal

---

**¿Necesitas ayuda?** Revisa los logs: `docker logs -f eltmko-elt-api`
