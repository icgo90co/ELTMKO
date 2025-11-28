# 🧪 Guía de Prueba - Configuración de Insights

Sigue estos pasos para probar la nueva funcionalidad.

## Prerequisitos

✅ Sistema ELT funcionando
✅ Docker en ejecución (si usas Docker)
✅ Navegador web actualizado

## Paso 1: Iniciar el Sistema

### Si usas Docker:
```bash
cd /workspaces/ELTMKO
./docker-start.sh
```

### Si usas ambiente local:
```bash
cd /workspaces/ELTMKO
source .venv/bin/activate
python api.py
```

Espera a que la consola muestre:
```
* Running on http://0.0.0.0:5000
```

## Paso 2: Abrir la Interfaz Web

Abre en tu navegador:
```
http://localhost:5000
```

## Paso 3: Acceder al Modal de Configuración

1. Busca la sección "📋 Tablas Disponibles para Sincronizar"
2. Haz click en el botón **"📊 Configurar Insights"**

Deberías ver un modal con estos campos:

```
┌─────────────────────────────────────────────┐
│ 📊 Configuración de Insights        [X]    │
├─────────────────────────────────────────────┤
│                                             │
│ Dimensión (Nivel de Agregación):           │
│ [account ▼]                                 │
│                                             │
│ Granularidad Temporal:                      │
│ [daily ▼]                                   │
│                                             │
│ Rango de Fechas:                            │
│ Fecha Inicio: [______]  Fecha Fin: [______] │
│ Últimos días: [30]                          │
│                                             │
│ Métricas a Incluir:                         │
│ ☑ Impresiones                               │
│ ☑ Clics                                     │
│ ☑ Gasto                                     │
│ ... más opciones                            │
│                                             │
│ [💾 Guardar]  [Cancelar]                    │
└─────────────────────────────────────────────┘
```

## Paso 4: Probar Cada Opción

### Prueba 4.1: Cambiar Dimensión

**Acción:**
1. Click en el selector "Dimensión"
2. Selecciona "Por Campaña"
3. Click "Guardar"

**Resultado esperado:**
- ✅ Alerta: "Configuración de insights guardada exitosamente"
- ✅ Modal se cierra
- ✅ En el archivo `config/config.yaml` aparece `level: campaign`

### Prueba 4.2: Cambiar Granularidad

**Acción:**
1. Click en "Configurar Insights"
2. Selecciona "Mensual" en Granularidad Temporal
3. Click "Guardar"

**Resultado esperado:**
- ✅ La próxima sincronización usará datos mensuales
- ✅ `time_increment: monthly` en `config/config.yaml`

### Prueba 4.3: Especificar Fechas

**Acción:**
1. Click en "Configurar Insights"
2. Ingresa:
   - Fecha Inicio: 2025-11-01
   - Fecha Fin: 2025-11-30
3. Click "Guardar"

**Resultado esperado:**
- ✅ Se guardan las fechas exactas
- ✅ Ignora el campo "Últimos días"
- ✅ En `config.yaml`: 
   ```yaml
   start_date: "2025-11-01"
   end_date: "2025-11-30"
   ```

### Prueba 4.4: Seleccionar Métricas

**Acción:**
1. Click en "Configurar Insights"
2. Desselecciona todas excepto:
   - Clics
   - Gasto
   - CPM
3. Click "Guardar"

**Resultado esperado:**
- ✅ Se guardan solo las métricas seleccionadas
- ✅ En `config.yaml`:
   ```yaml
   fields: ["clicks", "spend", "cpm"]
   ```

### Prueba 4.5: Combinación Completa

**Acción:**
1. Click en "Configurar Insights"
2. Configura como sigue:
   ```
   Dimensión:         Por AdSet
   Granularidad:      Diario
   Rango de Fechas:   Últimos 7 días
   Métricas:          ✓ Impresiones
                      ✓ Clics
                      ✓ Spend
                      ✓ CPM
   ```
3. Click "Guardar"

**Resultado esperado:**
- ✅ Todas las configuraciones se guardan
- ✅ Modal se cierra
- ✅ En `config.yaml` aparecen todos los valores

## Paso 5: Verificar Persistencia

**Acción:**
1. Abre el archivo `config/config.yaml`
2. Busca la sección `insights` bajo `tables`
3. Verifica que contiene:
   ```yaml
   - name: "insights"
     fields: [...]
     level: "adset"
     date_range: 7
     time_increment: "daily"
   ```

**Resultado esperado:**
- ✅ El archivo refleja todos los cambios hechos en la UI

## Paso 6: Probar API Directamente (Avanzado)

Abre una terminal y ejecuta:

### Obtener configuración actual
```bash
curl -X GET http://localhost:5000/api/insights/config | jq
```

**Resultado esperado:**
```json
{
  "success": true,
  "data": {
    "level": "adset",
    "date_range": 7,
    "start_date": null,
    "end_date": null,
    "time_increment": "daily",
    "fields": ["impressions", "clicks", "spend", "cpm"]
  }
}
```

### Cambiar configuración vía API
```bash
curl -X POST http://localhost:5000/api/insights/config \
  -H "Content-Type: application/json" \
  -d '{
    "level": "campaign",
    "time_increment": "monthly",
    "date_range": 90,
    "fields": ["impressions", "clicks", "spend", "reach"]
  }' | jq
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "Insights configuration updated successfully"
}
```

### Ver campos disponibles
```bash
curl -X GET http://localhost:5000/api/insights/available-fields | jq
```

## Paso 7: Ejecutar Pipeline con Nueva Configuración

**Acción:**
1. Vuelve a la interfaz web
2. En "Pipelines Activos", click en "▶️ Ejecutar Todos"

**Resultado esperado:**
- ✅ Pipeline se ejecuta
- ✅ Alertas muestran progreso
- ✅ Datos se sincronizan con nueva configuración
- ✅ En `config.yaml` se creó una tabla `facebook_ads_insights` (o similar)

**Para verificar:**
```bash
# Si usas Docker
docker exec eltmko-mysql-1 mysql -u eltuser -p elt_data -e "SELECT COUNT(*) as total FROM facebook_ads_insights LIMIT 5;"

# Si tienes MySQL local
mysql -u eltuser -p elt_data -e "SELECT COUNT(*) as total FROM facebook_ads_insights LIMIT 5;"
```

## Paso 8: Verificar Cambios en la Base de Datos

Dependiendo de tu configuración, deberías ver:

### Si configuraste nivel "campaign" + diario:
```
date_start      campaign_id     campaign_name    impressions  clicks
2025-11-27      123456          Summer Sale      10000        500
2025-11-27      123457          Winter Promo     8000         400
```

### Si configuraste nivel "account" + mensual:
```
date_start      impressions     clicks    spend
2025-11-01      300000          15000     $3000
2025-12-01      250000          12500     $2500
```

## Prueba de Estrés (Opcional)

**Acción:**
1. Cambia configuración múltiples veces rápidamente
2. Ej: campaign → ad → account → campaign
3. Verifica que no haya errores

**Resultado esperado:**
- ✅ Cada cambio se guarda correctamente
- ✅ No hay errores en la consola
- ✅ La configuración final es correcta

## Troubleshooting

### ❌ Modal no aparece
**Solución:**
- Verifica que JavaScript esté habilitado
- Abre la consola (F12) y busca errores
- Intenta refrescar la página (Ctrl+R)

### ❌ Error al guardar: "Error desconocido"
**Solución:**
- Revisa los logs: `docker logs elt-api`
- Verifica que al menos una métrica esté seleccionada
- Verifica que el archivo `config/config.yaml` sea editable

### ❌ Los cambios no se aplican
**Solución:**
- Espera a que se recargue el sistema
- Ejecuta el pipeline manualmente
- Reinicia el contenedor: `docker restart elt-api`

### ❌ Errores en la base de datos
**Solución:**
- Verifica conectividad a MySQL
- Revisa credenciales en el modal de configuración
- Verifica que la base de datos existe

## Checklista de Validación

Marca cuando completes cada prueba:

- [ ] Modal abre correctamente
- [ ] Puedo cambiar Dimensión
- [ ] Puedo cambiar Granularidad
- [ ] Puedo especificar fechas
- [ ] Puedo seleccionar métricas
- [ ] Los cambios se guardan en `config.yaml`
- [ ] Los cambios persisten al recargar la página
- [ ] API endpoint GET `/api/insights/config` funciona
- [ ] API endpoint POST `/api/insights/config` funciona
- [ ] Pipeline se ejecuta con nueva configuración
- [ ] Datos en base de datos reflejan configuración

## Reporte de Problemas

Si encuentras un problema:

1. Anota el paso donde ocurrió
2. Describe exactamente qué sucedió
3. Copia el error de la consola (F12)
4. Revisa los logs: `docker logs elt-api`
5. Reporta con esa información

---

**Duración estimada**: 15-20 minutos
**Nivel de dificultad**: Fácil
**Requisitos**: Solo navegador web

¡A probar! 🧪
