# 📊 Guía de Configuración de Insights

Esta guía te explica cómo configurar las dimensiones, métricas y períodos de tiempo para sincronizar datos de Facebook Ads Insights.

## Acceso a la Configuración

1. Abre la interfaz web: `http://localhost:5000`
2. En la sección "📋 Tablas Disponibles para Sincronizar"
3. Haz click en el botón **"📊 Configurar Insights"**

## Opciones Disponibles

### 1️⃣ Dimensión (Nivel de Agregación)

Selecciona cómo deseas agrupar los datos:

#### 📊 Nivel de Cuenta (Recomendado para principiantes)
```
- Agrupa TODAS las métricas a nivel de cuenta
- Un registro por período de tiempo
- Mejor para análisis generales
```

**Ejemplo de resultado:**
```
date_start    impressions  clicks  spend
2025-11-27    10,000       500     $100
2025-11-28    12,000       480     $95
```

#### 🎯 Por Campaña
```
- Métricas desglosadas por cada campaña
- Un registro por campaña por período
- Mejor para comparar rendimiento entre campañas
- Campos adicionales: campaign_id, campaign_name
```

**Ejemplo de resultado:**
```
date_start    campaign_name           impressions  clicks
2025-11-27    Summer Sale Campaign    5,000       250
2025-11-27    Winter Promotion        5,000       250
2025-11-28    Summer Sale Campaign    6,000       240
2025-11-28    Winter Promotion        6,000       240
```

#### 📌 Por Conjunto de Anuncios
```
- Métricas por cada conjunto de anuncios (AdSet)
- Un registro por adset por período
- Mejor para optimizar presupuestos
- Campos adicionales: adset_id, adset_name, campaign_id
```

#### 📢 Por Anuncio Individual
```
- Métricas para cada anuncio específico
- Máximo nivel de detalle
- Un registro por anuncio por período
- Mejor para análisis detallado de creativos
- Campos adicionales: ad_id, ad_name, adset_id, campaign_id
```

### 2️⃣ Granularidad Temporal

Cómo deseas desglosar los datos en el tiempo:

#### 📅 Diario (Recomendado)
```
- Un registro por cada día
- Mejor resolución
- Ideal para análisis de tendencias corto plazo
- Recomendado para campañas activas
```

#### 📆 Mensual
```
- Un registro por cada mes
- Datos agregados por mes
- Mejor para análisis de tendencias largo plazo
- Archivos más pequeños
- Menos registros en la base de datos
```

### 3️⃣ Rango de Fechas

Dos opciones:

#### Opción A: Especificar Fechas Exactas
```
Fecha Inicio: [2025-11-01]
Fecha Fin:    [2025-11-27]

Traerá datos de ese período exacto.
```

#### Opción B: Últimos Días
```
Últimos días: [30]

Traerá datos de los últimos 30 días.
Si dejas en blanco, usa 30 días por defecto.
```

⚠️ **Nota**: Si especificas fechas exactas, ignora "Últimos días".

### 4️⃣ Métricas a Incluir

Selecciona qué métricas deseas sincronizar:

| Métrica | Descripción | Ejemplo |
|---------|-------------|---------|
| **Impresiones** | Veces que se mostró el anuncio | 10,000 |
| **Clics** | Clics en el anuncio | 500 |
| **Gasto** | Dinero invertido | $100.50 |
| **Alcance** | Personas únicas que vieron el anuncio | 8,000 |
| **CTR** | Tasa de clics (%) | 5% |
| **CPC** | Costo por clic | $0.20 |
| **CPM** | Costo por mil impresiones | $10.00 |
| **Frecuencia** | Veces promedio mostrado a cada persona | 1.25 |

💡 **Tip**: Selecciona solo las que necesites para reducir tamaño de datos.

## Ejemplos de Configuración

### Ejemplo 1: Análisis Diario por Campaña

```
Dimensión:          Por Campaña
Granularidad:       Diario
Período:            Últimos 30 días
Métricas:           ✓ Impresiones
                    ✓ Clics
                    ✓ Gasto
                    ✓ CTR
```

**Resultado**: Verás cada campaña con sus métricas para cada día del último mes. Perfecto para análisis diarios.

### Ejemplo 2: Resumen Mensual de Cuenta

```
Dimensión:          Nivel de Cuenta
Granularidad:       Mensual
Período:            Últimos 365 días
Métricas:           ✓ Impresiones
                    ✓ Clics
                    ✓ Spend
                    ✓ Reach
                    ✓ CPM
```

**Resultado**: Un registro por mes con métricas agregadas de toda la cuenta. Perfecto para reportes ejecutivos.

### Ejemplo 3: Análisis Detallado por Anuncio

```
Dimensión:          Por Anuncio Individual
Granularidad:       Diario
Período:            Últimos 7 días
Métricas:           ✓ Clics
                    ✓ Gasto
                    ✓ CPC
                    ✓ CTR
```

**Resultado**: Verás cada anuncio con su desempeño diario. Ideal para encontrar creativos mejor/peor performantes.

## Cómo Cambiar la Configuración

1. Click en "📊 Configurar Insights"
2. Modifica los valores deseados
3. Click en "💾 Guardar Configuración"
4. El sistema recargará automáticamente

## Impacto en la Base de Datos

### Volumen de Datos
```
Nivel de Cuenta + Diario + 30 días     = ~30 registros
Por Campaña + Diario + 30 días         = ~30 × Num. Campañas
Por AdSet + Diario + 30 días           = ~30 × Num. AdSets
Por Anuncio + Diario + 30 días         = ~30 × Num. Anuncios
```

### Espacio en Base de Datos
```
Métricas selectas:    Menor volumen (recomendado)
Todas las métricas:   Mayor volumen
```

## Próxima Sincronización

Después de guardar:

1. Las cambios se guardan en `config/config.yaml`
2. La próxima ejecución del pipeline usará nuevos parámetros
3. Puedes ejecutar manualmente: Click "▶️ Ejecutar Todos"

## Resolución de Problemas

### ❌ "Error al guardar configuración"

**Solución**: 
- Verifica que al menos una métrica esté seleccionada
- Verifica que las fechas sean válidas
- Revisa los logs: `docker logs elt-api`

### ❌ "No hay datos nuevos después de cambiar configuración"

**Solución**:
- Espera a la próxima sincronización programada (cada hora)
- O ejecuta manualmente el pipeline
- Los datos viejos no se borran, solo se agregan nuevos registros

### ❌ "Tengo muchos datos y la sincronización es lenta"

**Solución**:
- Reduce el rango de fechas
- Reduce el número de métricas
- Aumenta la granularidad (cambia a mensual)
- Usa niveles menos detallados (Campaña en lugar de Anuncio)

## API Directa (Avanzado)

Si prefieres usar la API directamente:

```bash
# Obtener configuración actual
curl -X GET http://localhost:5000/api/insights/config

# Actualizar configuración
curl -X POST http://localhost:5000/api/insights/config \
  -H "Content-Type: application/json" \
  -d '{
    "level": "campaign",
    "time_increment": "daily",
    "date_range": 30,
    "fields": ["impressions", "clicks", "spend", "ctr"]
  }'

# Ver campos disponibles
curl -X GET http://localhost:5000/api/insights/available-fields
```

## Mejores Prácticas

✅ **DO:**
- Comienza con "Nivel de Cuenta" + "Diario"
- Selecciona solo las métricas que necesitas
- Usa "Últimos días" para datos recientes
- Revisa regularmente el tamaño de tus tablas

❌ **DON'T:**
- No configures períodos muy largos + nivel de detalle muy alto
- No selecciones todas las métricas si no las necesitas
- No cambies configuración muy frecuentemente (puede causar inconsistencias)

---

**Última actualización**: 28 de Noviembre, 2025
