# 🔍 DIAGNÓSTICO - Por Qué No Llegan Datos a MySQL

## 📊 Verificación en 5 Pasos

### Paso 1: Ver la Configuración Guardada
```bash
cat /workspaces/ELTMKO/config/config.yaml
```

**Deberías ver:**
```yaml
sources:
  - name: "facebook_ads"
    type: "facebook_ads"
    ...
    sync:
      tables:
        - name: "insights"
          level: "campaign"              ← ¿Está aquí?
          time_increment: "daily"        ← ¿Está aquí?
          fields: [                      ← ¿Está aquí?
            "date_start",
            "date_stop",
            "impressions",
            ...
          ]
          date_range: 30
```

**Si no ves `level`, `time_increment`, o `fields`** → Va al Paso 2

---

### Paso 2: Verificar que la API Está Guardando Correctamente

```bash
# Intenta guardar una nueva configuración por API
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
      "purchases"
    ]
  }'
```

**Deberías ver:**
```json
{
  "success": true,
  "message": "Insights configuration updated successfully"
}
```

**Si ves error** → Revisa logs: `docker logs -f eltmko-elt-api`

---

### Paso 3: Verifica que config.yaml se Actualizó
```bash
# Ver solo la sección insights
cat /workspaces/ELTMKO/config/config.yaml | grep -A 25 "insights"
```

**Deberías ver las nuevas métricas que acabas de enviar**

---

### Paso 4: Ejecutar Sincronización
```bash
# Opción A: Por navegador
Abre: http://localhost:5000
Click: "▶️ Ejecutar Todos"
Espera a que termine

# Opción B: Por API
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# Opción C: Por terminal
python main.py --mode once
```

**Espera a ver:**
```
INFO - Extracting insights from Facebook Ads...
INFO - Loaded X rows into facebook_ads_insights
```

---

### Paso 5: Verificar MySQL
```bash
# Conecta a MySQL
mysql -h mysql -u eltuser -peltpassword elt_data

# Ver estructura
DESCRIBE facebook_ads_insights;

# Ver datos
SELECT * FROM facebook_ads_insights LIMIT 1;

# Contar filas
SELECT COUNT(*) FROM facebook_ads_insights;
```

**Deberías ver:**
```
- Las nuevas columnas (purchases, leads, etc.)
- Al menos algunos registros
- Datos con fechas recientes
```

---

## 🐛 Problemas Comunes y Soluciones

### Problema 1: "No veo las nuevas columnas en MySQL"

**Causa:** Las tablas MySQL creadas anteriormente no se actualizan automáticamente

**Solución:**
```bash
# Opción A: Borra la tabla y recreala
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "DROP TABLE IF EXISTS facebook_ads_insights;"

# Luego ejecuta sincronización
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# Opción B: Manualmente agregar columnas
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "ALTER TABLE facebook_ads_insights ADD COLUMN purchases INT DEFAULT 0;"
```

---

### Problema 2: "El config.yaml tiene las métricas pero MySQL no"

**Causa:** La sincronización nunca se ejecutó desde que guardaste el config

**Solución:**
```bash
# Ejecuta manualmente
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads

# O desde el navegador
# http://localhost:5000 → Click "▶️ Ejecutar Todos"
```

---

### Problema 3: "Veo error en los logs"

**Ver logs:**
```bash
# Logs en tiempo real
docker logs -f eltmko-elt-api

# O desde archivo
tail -f /workspaces/ELTMKO/logs/elt.log

# Buscar errores
grep -i error /workspaces/ELTMKO/logs/elt.log | tail -20
```

**Errores comunes:**
```
"Error extracting insights" 
→ Problema con credenciales de Facebook

"Error connecting to MySQL"
→ MySQL no está disponible o credenciales incorrectas

"Unknown field"
→ Usaste un nombre de métrica que no existe en Facebook API
```

---

### Problema 4: "El config.yaml no se actualiza cuando uso el modal"

**Debug:**
```bash
# Abre el modal y selecciona métricas
# Guardas
# Verifica que se actualizó
cat /workspaces/ELTMKO/config/config.yaml | grep -A 20 insights

# Si NO se actualizó:
# 1. Ver logs del navegador (F12 → Console)
# 2. Ver respuesta de API
curl http://localhost:5000/api/insights/config
```

---

## ✅ Flujo Completo Paso a Paso

### Paso 1: Abre el Modal
```
http://localhost:5000
→ Click "📊 Configurar Insights"
```

### Paso 2: Selecciona Configuración
```
Dimensión: campaign
Granularidad: daily
Período: 30 días
Métricas: impressions, clicks, spend, purchases
```

### Paso 3: Guarda
```
Click "💾 Guardar Configuración"
Verás: ✅ "Configuración guardada exitosamente"
```

### Paso 4: Verifica que se Guardó
```bash
cat /workspaces/ELTMKO/config/config.yaml | grep -A 20 insights
# Deberías ver: level, time_increment, fields con tus selecciones
```

### Paso 5: Ejecuta Sincronización
```
http://localhost:5000
→ Click "▶️ Ejecutar Todos"
Espera a que termine
```

### Paso 6: Verifica MySQL
```bash
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SELECT * FROM facebook_ads_insights LIMIT 1;"
```

**Deberías ver:**
- Columnas: campaign_id, impressions, clicks, spend, purchases
- Datos recientes

---

## 🔧 Comandos Útiles

### Ver configuración actual
```bash
curl http://localhost:5000/api/insights/config | jq
```

### Ver métricas disponibles
```bash\ncurl http://localhost:5000/api/insights/available-fields | jq '.data.metrics | keys' | head -30
```

### Ejecutar sincronización manualmente
```bash
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads | jq
```

### Ver datos en MySQL
```bash
mysql -h mysql -u eltuser -peltpassword elt_data << EOF
SELECT COUNT(*) as total_rows FROM facebook_ads_insights;
SELECT COUNT(DISTINCT campaign_id) as campaigns FROM facebook_ads_insights;
SELECT MAX(date_start) as latest_date FROM facebook_ads_insights;
SHOW COLUMNS FROM facebook_ads_insights;
EOF
```

### Ver logs
```bash
# Últimas 50 líneas
tail -50 /workspaces/ELTMKO/logs/elt.log

# En tiempo real
tail -f /workspaces/ELTMKO/logs/elt.log

# Solo errores
grep ERROR /workspaces/ELTMKO/logs/elt.log
```

---

## 📋 Checklist de Verificación

- [ ] ¿El config.yaml tiene `level`, `time_increment`, `fields`?
- [ ] ¿Ejecutaste la sincronización?
- [ ] ¿Esperaste a que terminara?
- [ ] ¿Las tablas en MySQL existen?
- [ ] ¿Las tablas tienen las nuevas columnas?
- [ ] ¿Hay datos en las tablas?

---

## 🚨 Si Nada Funciona

### Paso 1: Reinicia todo
```bash
docker-compose restart
sleep 10
curl http://localhost:5000/health
```

### Paso 2: Verifica credenciales
```bash
cat .env | grep FACEBOOK
cat .env | grep MYSQL
```

### Paso 3: Ver logs detallados
```bash
docker logs eltmko-elt-api
docker logs eltmko-mysql
```

### Paso 4: Reset (⚠️ Elimina datos)
```bash
docker-compose down -v
docker-compose up -d
docker-compose logs -f
```

---

## 📞 Información de Contacto para Debugging

Cuando pidas ayuda, incluye:
1. Output de: `cat config/config.yaml | grep -A 20 insights`
2. Output de: `curl http://localhost:5000/api/insights/config | jq`
3. Últimas líneas de logs: `tail -50 logs/elt.log`
4. Output de MySQL: `SELECT COUNT(*) FROM facebook_ads_insights;`

---

**¿Todavía no funciona?** Revisa `/FIX_MYSQL_NO_DATA.md` para más soluciones.
