# ✅ INSTRUCCIONES - Datos a MySQL CON NUEVAS MÉTRICAS

## Tu Situación Actual
```
✅ Tienes el modal con 42+ métricas
✅ Puedes seleccionar las que quieras
❌ PERO: Los datos no llegan a MySQL con esas métricas
```

## La Solución en 2 Minutos

### Opción 1: MÁS SIMPLE (Recomendado)

#### Paso 1: Abre el Modal
```
http://localhost:5000
→ Click "📊 Configurar Insights"
```

#### Paso 2: Selecciona Métricas
```
En "Métricas a Incluir" marca las que necesites:

EJEMPLO para E-Commerce:
☑ date_start
☑ date_stop
☑ impressions
☑ clicks
☑ spend
☑ reach
☑ purchases       ← IMPORTANTE
☑ cost_per_purchase ← IMPORTANTE
☑ purchase_roas   ← IMPORTANTE
☑ cpc
☑ cpm
```

#### Paso 3: Guarda
```
Click: "💾 Guardar Configuración"
Verás: ✅ "Configuración guardada exitosamente"
```

#### Paso 4: Ejecuta Sincronización
```
Click: "▶️ Ejecutar Todos"
Espera a que termine (1-5 minutos)
Verás: ✅ "Pipelines ejecutados correctamente"
```

#### Paso 5: Verifica en MySQL
```bash
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SELECT date_start, campaign_name, purchases, cost_per_purchase FROM facebook_ads_insights LIMIT 3;"
```

**Deberías ver datos con las nuevas columnas** ✅

---

### Opción 2: MANUAL (Si el Modal No Funciona)

#### Paso 1: Editar config.yaml
```bash
nano /workspaces/ELTMKO/config/config.yaml
```

#### Paso 2: Busca esta sección (aproximadamente línea 33)
```yaml
        - name: "insights"
          fields: ["date_start", "date_stop", "impressions", "clicks", "spend", "reach", "ctr", "cpc", "cpm"]
          date_range: 30
```

#### Paso 3: Reemplaza por esto
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
            "ctr",
            "cpc",
            "cpm",
            "purchases",
            "cost_per_purchase",
            "purchase_roas",
            "leads",
            "cost_per_lead",
            "post_engagement",
            "video_views"
          ]
          date_range: 30
```

#### Paso 4: Guarda
```
Ctrl+O → Enter → Ctrl+X
```

#### Paso 5: Ejecuta Sincronización
```bash
# Opción A: Desde navegador
http://localhost:5000 → Click "▶️ Ejecutar Todos"

# Opción B: Desde terminal
curl -X POST http://localhost:5000/api/pipelines/run/facebook_ads
```

#### Paso 6: Verifica
```bash
mysql -h mysql -u eltuser -peltpassword elt_data \
  -e "SELECT * FROM facebook_ads_insights LIMIT 1;"
```

---

## 📊 Qué Esperar

### ANTES (Sin cambios)
```sql
mysql> DESCRIBE facebook_ads_insights;
┌─────────────┬─────────┐
│ Field       │ Type    │
├─────────────┼─────────┤
│ date_start  │ VARCHAR │
│ date_stop   │ VARCHAR │
│ impressions │ BIGINT  │
│ clicks      │ BIGINT  │
│ spend       │ DECIMAL │
│ reach       │ BIGINT  │
│ ctr         │ DECIMAL │
│ cpc         │ DECIMAL │
│ cpm         │ DECIMAL │
│ frequency   │ DECIMAL │
└─────────────┴─────────┘
```

### DESPUÉS (Con nuevas métricas)
```sql\nmysql> DESCRIBE facebook_ads_insights;\n┌──────────────────────┬─────────┐\n│ Field                │ Type    │\n├──────────────────────┼─────────┤\n│ date_start           │ VARCHAR │\n│ date_stop            │ VARCHAR │\n│ campaign_id          │ VARCHAR │\n│ campaign_name        │ VARCHAR │\n│ impressions          │ BIGINT  │\n│ clicks               │ BIGINT  │\n│ spend                │ DECIMAL │\n│ reach                │ BIGINT  │\n│ frequency            │ DECIMAL │\n│ ctr                  │ DECIMAL │\n│ cpc                  │ DECIMAL │\n│ cpm                  │ DECIMAL │\n│ purchases            │ BIGINT  │ ← NUEVO\n│ cost_per_purchase    │ DECIMAL │ ← NUEVO\n│ purchase_roas        │ DECIMAL │ ← NUEVO\n│ leads                │ BIGINT  │ ← NUEVO\n│ cost_per_lead        │ DECIMAL │ ← NUEVO\n│ post_engagement      │ BIGINT  │ ← NUEVO\n│ video_views          │ BIGINT  │ ← NUEVO\n└──────────────────────┴─────────┘\n```\n\n---\n\n## 🎯 Ejemplo de Datos en MySQL\n\nDespués de sincronizar, consulta:\n```sql\nSELECT \n  date_start,\n  campaign_name,\n  impressions,\n  clicks,\n  spend,\n  purchases,\n  cost_per_purchase,\n  purchase_roas,\n  leads,\n  cost_per_lead\nFROM facebook_ads_insights\nWHERE date_start = '2025-11-28'\nORDER BY campaign_name;\n```\n\n**Resultado esperado:**\n```\n┌────────────┬──────────────┬─────────────┬────────┬────────┬───────────┬──────────────────┬────────────────┬───────┬──────────────┐\n│ date_start │ campaign_name│ impressions │ clicks │ spend  │ purchases │ cost_per_purchase│ purchase_roas  │ leads │ cost_per_lead│\n├────────────┼──────────────┼─────────────┼────────┼────────┼───────────┼──────────────────┼────────────────┼───────┼──────────────┤\n│ 2025-11-28 │ Campaign A   │ 18000       │ 900    │ $180   │ 125       │ $1.44            │ 5.56           │ 30    │ $6.00        │\n│ 2025-11-28 │ Campaign B   │ 12000       │ 600    │ $120   │ 80        │ $1.50            │ 5.33           │ 20    │ $6.00        │\n└────────────┴──────────────┴─────────────┴────────┴────────┴───────────┴──────────────────┴────────────────┴───────┴──────────────┘\n```\n\n**¡PERFECTO!** Ahora tienes todas las métricas en MySQL ✅\n\n---\n\n## 🔧 Si Algo No Funciona\n\n### P: El config.yaml no se actualiza\n**R:** Abre el modal nuevamente, selecciona, y guarda\n\n### P: La sincronización dice \"0 rows\"\n**R:** Verifica credenciales de Facebook:\n```bash\ncat .env | grep FACEBOOK\n```\n\n### P: MySQL dice \"Table doesn't exist\"\n**R:** Es normal la primera vez. Ejecuta sincronización y la crea automáticamente\n\n### P: Nada funciona\n**R:** Reinicia todo:\n```bash\ndocker-compose restart\nsleep 10\ncurl http://localhost:5000/health\n```\n\n---\n\n## 📋 Checklist Final\n\n- [ ] Abrí el modal ✓\n- [ ] Seleccioné métricas ✓\n- [ ] Hice click \"Guardar\" ✓\n- [ ] Ejecuté sincronización ✓\n- [ ] Esperé a que terminara ✓\n- [ ] Verifiqué en MySQL ✓\n- [ ] Vi nuevas columnas ✓\n- [ ] Vi datos en las nuevas columnas ✓\n\n**Si todo ✓ → ¡FELICIDADES! Está listo** 🎉\n\n---\n\n## 🎓 Para Entender Mejor\n\n- `FLOW_DIAGRAM.md` - Diagrama completo del flujo\n- `DIAGNOSTIC_GUIDE.md` - Troubleshooting detallado\n- `FIX_MYSQL_NO_DATA.md` - Soluciones específicas\n- `QUICK_FIX_MYSQL.md` - Resumen ejecutivo\n\n---\n\n**¡Ahora a sincronizar!** 🚀\n"
