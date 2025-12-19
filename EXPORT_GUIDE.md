# 📥 Guía de Exportación y Filtrado de Datos

## Resumen de la Nueva Funcionalidad

Se ha implementado un sistema completo de **filtrado y exportación de datos** que te permite:

✅ **Seleccionar qué tabla exportar** (Campañas, AdSets, Ads, Insights)  
✅ **Elegir columnas específicas** para incluir en la exportación  
✅ **Filtrar por rango de fechas** (date_start y date_stop)  
✅ **Aplicar filtros personalizados** a cualquier campo  
✅ **Vista previa de datos** antes de exportar  
✅ **Descargar en formato CSV**

---

## 🚀 Cómo Usar la Función de Exportación

### Paso 1: Acceder a la Exportación

Hay **3 formas** de acceder:

1. **Desde el menú lateral izquierdo**: Click en "Exportar Datos" 
2. **Desde el panel principal**: Click en el botón verde "Exportar Datos"
3. **Desde la sección de tablas**: Próximamente en cada tabla

### Paso 2: Configurar la Exportación

#### 1. **Seleccionar Tabla**
```
Opciones disponibles:
├── facebook_ads_campaigns (Campañas)
├── facebook_ads_adsets (Conjuntos de Anuncios)
├── facebook_ads_ads (Anuncios)
└── facebook_ads_insights (Métricas/Insights) ⭐ Más usado
```

#### 2. **Filtrar por Fechas** (Opcional)
- **Fecha Inicio**: Primera fecha a incluir
- **Fecha Fin**: Última fecha a incluir
- **Nota**: Solo aplica a tablas con `date_start` y `date_stop`

#### 3. **Seleccionar Columnas**
- Por defecto, todas las columnas están seleccionadas (excepto las internas `_elt_*`)
- Usa "Seleccionar Todas" o "Deseleccionar Todas" para control rápido
- Marca solo las columnas que necesitas para un CSV más limpio

#### 4. **Agregar Filtros Adicionales** (Opcional)
- Click en "+ Agregar Filtro"
- Selecciona el campo a filtrar
- Ingresa el valor exacto
- Puedes agregar múltiples filtros

**Ejemplo de filtros:**
```
Campo: campaign_id  →  Valor: 123456789
Campo: status       →  Valor: ACTIVE
```

#### 5. **Límite de Registros**
- Por defecto: 10,000 registros
- Máximo: 100,000 registros por exportación

### Paso 3: Vista Previa (Recomendado)

Antes de exportar, click en **"Vista Previa"**:
- Muestra los primeros 10 registros
- Verifica que los filtros funcionen correctamente
- Confirma que seleccionaste las columnas correctas

### Paso 4: Descargar CSV

Click en **"Descargar CSV"**:
- Se descargará automáticamente un archivo `.csv`
- Nombre del archivo: `{tabla}_{fecha_hora}.csv`
- Abre con Excel, Google Sheets, o cualquier herramienta de análisis

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Exportar Insights por Día del Último Mes

```
Tabla: facebook_ads_insights
Fecha Inicio: 2025-11-19
Fecha Fin: 2025-12-19
Columnas: ✓ date_start, ✓ impressions, ✓ clicks, ✓ spend, ✓ ctr, ✓ cpc
Límite: 10000
```

### Ejemplo 2: Exportar Solo Campañas Activas

```
Tabla: facebook_ads_campaigns
Columnas: ✓ id, ✓ name, ✓ status, ✓ objective
Filtro 1: status = ACTIVE
Límite: 1000
```

### Ejemplo 3: Exportar Métricas de una Campaña Específica

```
Tabla: facebook_ads_insights
Fecha Inicio: 2025-01-01
Fecha Fin: 2025-12-31
Columnas: ✓ date_start, ✓ campaign_name, ✓ impressions, ✓ spend
Filtro 1: campaign_id = 120212345678901234
Límite: 10000
```

---

## 🔧 Características Técnicas

### Endpoints API Nuevos

#### 1. **GET /api/tables/{table}/columns**
Obtiene la lista de columnas disponibles en una tabla.

**Ejemplo:**
```bash
curl http://localhost:5000/api/tables/facebook_ads_insights/columns
```

**Respuesta:**
```json
{
  "success": true,
  "data": [
    {"name": "date_start", "type": "date", "nullable": false},
    {"name": "impressions", "type": "bigint", "nullable": true},
    ...
  ]
}
```

#### 2. **POST /api/data/query**
Consulta datos con filtros (para vista previa).

**Body:**
```json
{
  "table": "facebook_ads_insights",
  "columns": ["date_start", "impressions", "clicks"],
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "filters": {
    "campaign_id": "123456789"
  },
  "limit": 100
}
```

**Respuesta:**
```json
{
  "success": true,
  "data": [...],
  "count": 45
}
```

#### 3. **POST /api/data/export**
Exporta datos a CSV con filtros.

**Body:** (mismo formato que `/api/data/query` pero sin `limit`)

**Respuesta:** Archivo CSV descargable

---

## 💡 Tips y Mejores Prácticas

### ✅ Recomendaciones

1. **Usa Vista Previa primero**: Siempre verifica los datos antes de exportar
2. **Selecciona solo columnas necesarias**: Archivos más pequeños y manejables
3. **Aplica filtros de fecha**: Reduce el volumen de datos
4. **Exporta por períodos**: En vez de todo el histórico, exporta por meses
5. **Verifica el límite**: Si necesitas más de 100k registros, divide en varias exportaciones

### ⚠️ Limitaciones Actuales

- **Máximo 100,000 registros** por exportación
- **Filtros exactos únicamente**: No soporta operadores como "mayor que" o "contiene"
- **Solo formato CSV**: No disponible Excel o JSON (próximamente)
- **Filtros de fecha solo en tablas con date_start/date_stop**

### 🔮 Próximas Mejoras

- [ ] Exportación directa desde cada tabla en el dashboard
- [ ] Filtros avanzados (>, <, >=, <=, LIKE, IN)
- [ ] Exportación en múltiples formatos (Excel, JSON, Parquet)
- [ ] Guardar configuraciones de filtros favoritas
- [ ] Programar exportaciones automáticas
- [ ] Enviar exportaciones por email

---

## 🐛 Solución de Problemas

### Problema: "No data found with the specified filters"
**Solución:** 
- Verifica que los filtros sean correctos
- Revisa el rango de fechas
- Confirma que hay datos en la tabla con esos criterios

### Problema: "Table name is required"
**Solución:** Selecciona una tabla del dropdown antes de exportar

### Problema: El CSV se descarga vacío
**Solución:**
- Usa Vista Previa para verificar que hay datos
- Revisa los filtros de fecha
- Asegúrate de que la tabla tenga datos

### Problema: Columnas no se cargan
**Solución:**
- Selecciona primero la tabla
- Espera unos segundos mientras se cargan
- Recarga la página si persiste

---

## 📞 Soporte

Si encuentras problemas o necesitas ayuda:

1. **Revisa los logs de la API**: `logs/elt.log`
2. **Verifica la consola del navegador**: F12 > Console
3. **Prueba los endpoints directamente**: Usa `test_export_api.py`

```bash
python test_export_api.py
```

---

## 🎯 Resumen Rápido

```
1. Click en "Exportar Datos" 📥
2. Selecciona la tabla 📊
3. Configura filtros y fechas 📅
4. Elige columnas ☑️
5. Vista previa (opcional) 👁️
6. Descargar CSV ⬇️
```

¡Disfruta de tu nueva herramienta de exportación! 🎉
