# 🎯 Configuración Dinámica de Insights - Resumen Ejecutivo

## ¿Qué es lo Nuevo?

Ahora puedes configurar desde la web cómo traer datos de Facebook Ads Insights sin editar archivos:

### Antes (Complicado):
```yaml
# Editar config.yaml manualmente
- name: "insights"
  fields: ["impressions", "clicks", "spend"]  # Fijo
  date_range: 30  # Fijo
```

### Ahora (Fácil):
```
1. Click "📊 Configurar Insights"
2. Selecciona opciones en el modal
3. Click "Guardar"
4. ¡Listo!
```

## Las 4 Opciones de Configuración

### 1. 📊 Dimensión (¿A qué nivel agregar datos?)

| Opción | Ejemplo | Usa cuando |
|--------|---------|-----------|
| **Cuenta** | Todas las campañas juntas | Necesitas visión general |
| **Campaña** | Cada campaña por separado | Comparas rendimiento entre campañas |
| **AdSet** | Cada conjunto de anuncios | Optimizas presupuestos |
| **Anuncio** | Cada anuncio individual | Analizas creativos específicos |

### 2. 📅 Granularidad Temporal (¿Cómo desglosar el tiempo?)

| Opción | Resultado | Usa cuando |
|--------|-----------|-----------|
| **Diario** | Un registro por día | Necesitas detalle diario |
| **Mensual** | Un registro por mes | Prefieres menos datos |

### 3. 📆 Rango de Fechas (¿Qué período?)

```
Opción A: Últimos X días
  └─ Ejemplo: Últimos 30 días

Opción B: Período específico
  └─ Desde: 2025-11-01
  └─ Hasta: 2025-11-30
```

### 4. 📊 Métricas (¿Qué datos traer?)

Selecciona solo lo que necesites:
- ✓ Impresiones (views)
- ✓ Clics
- ✓ Gasto
- ✓ Alcance (unique viewers)
- ✓ CTR (Click Through Rate %)
- ✓ CPC (Costo por Clic)
- ✓ CPM (Costo por Mil)
- ✓ Frecuencia (avg views per person)

## Dónde Está

En la interfaz web (`http://localhost:5000`):

1. Busca: "📋 Tablas Disponibles para Sincronizar"
2. Haz click en: "📊 Configurar Insights"
3. ¡Listo!

## Ejemplos Listos para Usar

### 📈 Análisis Diario por Campaña
```
Dimensión:     Por Campaña
Granularidad:  Diario
Período:       Últimos 30 días
Métricas:      Impresiones, Clics, Gasto, CTR
```
👉 **Para**: Monitoreo diario de campañas

### 📊 Resumen Mensual de Toda la Cuenta
```
Dimensión:     Cuenta
Granularidad:  Mensual
Período:       Últimos 365 días
Métricas:      Impresiones, Clics, Spend, Alcance, CPM
```
👉 **Para**: Reportes ejecutivos

### 🔍 Análisis Detallado de Anuncios (Últimos 7 Días)
```
Dimensión:     Anuncio Individual
Granularidad:  Diario
Período:       Últimos 7 días
Métricas:      Clics, Gasto, CPC, CTR
```
👉 **Para**: Optimizar creativos

## Impacto en tu Base de Datos

**Volumen = Dimensión × Días × Métricas**

```
Cuenta + 30 días diario        = ~30 registros     ✅ Pequeño
Campaña + 30 días diario       = ~30-300 registros ✅ Mediano
AdSet + 30 días diario         = ~300+ registros   ⚠️ Grande
Anuncio + 90 días diario       = ~1000+ registros  ❌ Muy grande
```

💡 **Tip**: Selecciona solo métricas que necesites para reducir tamaño

## Flujo de Uso

```
┌─────────────────┐
│ Interfaz Web    │
│ 📊 Config Modal │
└────────┬────────┘
         │
         ↓ Click "Guardar"
         │
    ┌────┴─────────┐
    │ POST API     │
    │ /insights... │
    └────┬─────────┘
         │
         ↓ Actualiza config.yaml
         │
    ┌────┴──────────────┐
    │ Próxima           │
    │ Sincronización    │
    │ usa nuevos datos  │
    └────┬──────────────┘
         │
         ↓
    ┌────┴──────────────┐
    │ Nueva data en     │
    │ MySQL con nuevos  │
    │ parámetros        │
    └────────────────────┘
```

## API (Si Prefieres Terminal)

```bash
# Ver configuración actual
curl http://localhost:5000/api/insights/config

# Cambiar configuración
curl -X POST http://localhost:5000/api/insights/config \
  -H "Content-Type: application/json" \
  -d '{
    "level": "campaign",
    "time_increment": "daily",
    "date_range": 30,
    "fields": ["impressions", "clicks", "spend"]
  }'
```

## Mejores Prácticas

✅ **Hacer**:
- Comienza con "Cuenta" + "Diario"
- Luego expande a más detalle si necesitas
- Selecciona solo métricas necesarias
- Usa "últimos X días" para datos recientes

❌ **No hacer**:
- No uses "Anuncio Individual" + "90 días" al principio
- No selecciones todas las métricas si no las necesitas
- No cambies configuración muy frecuentemente

## Archivos Modificados

| Archivo | Qué cambió |
|---------|-----------|
| `src/extractors/facebook_ads_extractor.py` | Más opciones en `extract_insights()` |
| `api.py` | +3 nuevos endpoints |
| `static/index.html` | +1 modal, +4 funciones JS |
| `config/config.yaml` | Nuevos campos opcionales |

## Archivos de Documentación Nuevos

1. **`INSIGHTS_CONFIGURATION_GUIDE.md`** - Guía detallada completa
2. **`INSIGHTS_CHANGES_SUMMARY.md`** - Cambios técnicos
3. **`TESTING_GUIDE.md`** - Cómo probar todas las funciones
4. **`INSIGHTS_EXECUTIVE_SUMMARY.md`** - Este archivo

## Compatibilidad

✅ Totalmente compatible con configuraciones antigas
✅ Valores por defecto mantienen comportamiento anterior
✅ No afecta tablas de base de datos existentes

## Próximos Pasos

1. **Prueba básica** → Lee `TESTING_GUIDE.md`
2. **Entiende opciones** → Lee `INSIGHTS_CONFIGURATION_GUIDE.md`
3. **Ve detalles técnicos** → Lee `INSIGHTS_CHANGES_SUMMARY.md`

## Preguntas Frecuentes

**P: ¿Qué pasa si cambio la configuración?**
R: La próxima sincronización usará los nuevos parámetros. Los datos viejos permanecen.

**P: ¿Pierdo datos si cambio la dimensión?**
R: No, cada cambio crea nuevos registros. Los viejos se mantienen.

**P: ¿Cuál es la mejor configuración para empezar?**
R: Dimensión="Cuenta", Granularidad="Diario", Período="30 días"

**P: ¿Cómo sé si mi configuración causa muchos datos?**
R: Ve la tabla en `INSIGHTS_CONFIGURATION_GUIDE.md` que muestra volumen

**P: ¿Se guardan los cambios automáticamente?**
R: Sí, se guardan en `config/config.yaml` cuando haces click "Guardar"

**P: ¿Puedo usar API en lugar del modal?**
R: Sí, hay 3 nuevos endpoints en `api.py`

---

**Creado**: 28 de Noviembre, 2025
**Estado**: ✅ Listo para usar
**Documentación**: Completa
