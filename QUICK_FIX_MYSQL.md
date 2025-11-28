# 🚀 SOLUCIÓN RÁPIDA - Datos en MySQL

## El Problema
> "No veo datos de las nuevas métricas en MySQL"

## La Solución
**3 pasos simples:**

---

## Paso 1️⃣: Actualizar Configuración

### Opción A: Desde el Modal (Recomendado)
```
1. Abre: http://localhost:5000
2. Click: "📊 Configurar Insights"
3. Selecciona: Las métricas que quieras
   Ej: impressions, clicks, spend, purchases, leads
4. Click: "💾 Guardar Configuración"
5. Ver: ✅ Confirmación
```

### Opción B: Editar File Directamente
```bash
nano /workspaces/ELTMKO/config/config.yaml
```

Busca la sección `insights` y actualiza:
```yaml
- name: "insights"
  level: "campaign"           # ← Agregado
  time_increment: "daily"     # ← Agregado
  fields: [
    "date_start",
    "date_stop", 
    "impressions",
    "clicks",
    "spend",
    "purchases",              # ← NUEVO
    "leads",                  # ← NUEVO
    "cost_per_purchase",      # ← NUEVO
    "video_views"             # ← NUEVO
  ]
  date_range: 30
```

**Guarda:** Ctrl+O, Enter, Ctrl+X

---

## Paso 2️⃣: Ejecutar Sincronización

### Opción A: Desde el Navegador
```
http://localhost:5000
→ Click: "▶️ Ejecutar Todos"
→ Espera a que termine
```

### Opción B: Desde Terminal
```bash
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads
```

### Opción C: Por Python
```bash
python /workspaces/ELTMKO/main.py --mode once
```

---

## Paso 3️⃣: Verificar en MySQL

```bash
# Conecta a MySQL
mysql -h mysql -u eltuser -peltpassword elt_data

# Ver si hay datos
SELECT COUNT(*) FROM facebook_ads_insights;

# Ver estructura
DESCRIBE facebook_ads_insights;

# Ver primeros datos
SELECT date_start, campaign_name, impressions, clicks, purchases FROM facebook_ads_insights LIMIT 3;
```

**Deberías ver:**
```
- Número de registros: > 0
- Columnas: campaign_name, purchases, leads, etc.
- Datos con fechas recientes
```

---

## ✅ ¿Funciona Ahora?

| Síntoma | Solución |
|---------|----------|
| ✅ Veo datos en MySQL | **¡Listo!** Las métricas se sincronizan correctamente |
| ❌ No veo datos | Ejecuta sincronización nuevamente (Paso 2) |
| ❌ No veo nuevas columnas | Borra tabla: `DROP TABLE facebook_ads_insights;` luego sincroniza |
| ❌ Error de conexión | Verifica credenciales en `.env` |

---

## 🎯 Ejemplos de Configuración

### E-Commerce
```yaml
fields: [
  "date_start", "date_stop",
  "campaign_id", "campaign_name",
  "impressions", "clicks", "spend",
  "purchases",           # ← Vendas
  "cost_per_purchase",   # ← Costo
  "purchase_roas"        # ← ROI
]
```

### Generador de Leads
```yaml
fields: [
  "date_start", "date_stop",
  "campaign_id", "campaign_name",
  "impressions", "clicks", "spend",
  "leads",           # ← Contactos
  "cost_per_lead"    # ← Costo
]
```

### Video Marketing
```yaml
fields: [
  "date_start", "date_stop",
  "ad_id", "ad_name",
  "impressions", "clicks",
  "video_views",                  # ← Vistas
  "video_play_actions",           # ← Reproducciones
  "video_avg_time_watched_actions" # ← Duración promedio
]
```

---

## 📊 Resultado Final

**Después de sincronizar, en MySQL verás:**

```sql
mysql> SELECT * FROM facebook_ads_insights LIMIT 2;

┌─────────────┬──────────────┬─────────────┬────────┬────────┬───────────┬──────────────────┐
│ date_start  │ campaign_name│ impressions │ clicks │ spend  │ purchases │ cost_per_purchase│
├─────────────┼──────────────┼─────────────┼────────┼────────┼───────────┼──────────────────┤
│ 2025-11-27  │ Campaign A   │ 15000       │ 750    │ $150   │ 100       │ $1.50            │
│ 2025-11-28  │ Campaign A   │ 18000       │ 900    │ $180   │ 125       │ $1.44            │
└─────────────┴──────────────┴─────────────┴────────┴────────┴───────────┴──────────────────┘
```

---

## 🔗 Documentación

- `DIAGNOSTIC_GUIDE.md` - Guía completa de troubleshooting
- `FIX_MYSQL_NO_DATA.md` - Soluciones detalladas
- `AVAILABLE_METRICS.md` - Lista de todas las métricas

---

**¡Listo!** Ahora tus datos llegarán a MySQL con todas las métricas. 🎉
