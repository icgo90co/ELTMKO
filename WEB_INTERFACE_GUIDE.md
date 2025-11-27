# 🖥️ Guía de la Interfaz Web

## Acceso

Abrir en navegador: **http://localhost:5000**

## Secciones Principales

### 1. 📊 Pipelines Activos

Muestra todos los pipelines configurados y permite:
- Ver el estado de cada pipeline
- **▶️ Ejecutar Todos**: Ejecuta todos los pipelines
- **▶️ Ejecutar**: Ejecuta un pipeline específico
- **🔄 Actualizar**: Recarga la información

### 2. 📥 Fuentes de Datos

Muestra las fuentes configuradas (Facebook Ads, etc.)

**⚙️ Configurar Facebook Ads**:
1. Click en "⚙️ Configurar"
2. Completar el formulario:
   - **App ID**: ID de tu aplicación de Facebook
   - **App Secret**: Secret de tu aplicación
   - **Access Token**: Token de acceso de Facebook Ads
   - **Ad Account ID**: ID de tu cuenta de anuncios (ej: act_123456789)
3. Activar checkbox "Activar esta fuente"
4. Click en "💾 Guardar Configuración"

**¿Dónde obtener las credenciales?**
- Ve a [Facebook Developers](https://developers.facebook.com/)
- Crea o selecciona tu aplicación
- En configuración, encontrarás App ID y App Secret
- Para el Access Token, usa la herramienta [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- El Ad Account ID lo encuentras en Facebook Ads Manager (URL o configuración de cuenta)

### 3. 📤 Destinos

Muestra los destinos configurados (MySQL, etc.)

**⚙️ Configurar MySQL**:
1. Click en "⚙️ Configurar"
2. Completar el formulario:
   - **Host**: `mysql` (en Docker) o `localhost` (instalación local)
   - **Puerto**: `3306` (por defecto)
   - **Usuario**: Usuario de MySQL (ej: `eltuser`)
   - **Contraseña**: Contraseña del usuario
   - **Base de Datos**: `elt_data` (por defecto)
3. Activar checkbox "Activar este destino"
4. Click en "💾 Guardar Configuración"

### 4. 📋 Tablas Disponibles para Sincronizar

Muestra todas las tablas que se pueden sincronizar desde Facebook Ads:

| Tabla | Descripción | Datos |
|-------|-------------|-------|
| **campaigns** | Campañas publicitarias | id, name, status, objective, created_time |
| **adsets** | Conjuntos de anuncios | id, name, status, campaign_id, budget |
| **ads** | Anuncios individuales | id, name, status, adset_id, creative |
| **insights** | Métricas y estadísticas | impressions, clicks, spend, reach, ctr, cpc |

**Activar/Desactivar tablas**:
- Usa el toggle switch (interruptor) al lado de cada tabla
- Verde = Activada (se sincronizará)
- Gris = Desactivada (no se sincronizará)

### 5. 📊 Datos Sincronizados

Muestra estadísticas de los datos ya sincronizados:
- **Número de registros** en cada tabla
- **Última sincronización**: Fecha y hora del último sync
- **Estado visual**: Código de colores (verde = datos recientes)

## Flujo de Trabajo Típico

### Primera Vez

1. **Configurar Facebook Ads**
   - Click en "⚙️ Configurar" en Fuentes
   - Ingresar credenciales
   - Guardar

2. **Verificar MySQL**
   - Click en "⚙️ Configurar" en Destinos
   - Verificar/ajustar configuración
   - Guardar

3. **Seleccionar Tablas**
   - En "Tablas Disponibles"
   - Activar las tablas que quieras sincronizar
   - Por defecto todas están activadas

4. **Ejecutar Primera Sincronización**
   - Click en "▶️ Ejecutar Todos" en Pipelines
   - Esperar a que termine
   - Ver resultados en "Datos Sincronizados"

### Uso Regular

1. **Ver Estado**
   - Revisar "Datos Sincronizados"
   - Verificar fechas de última sincronización

2. **Ejecutar Sync Manual**
   - Click en "▶️ Ejecutar" en el pipeline deseado
   - O "▶️ Ejecutar Todos"

3. **Actualizar Vista**
   - Click en "🔄 Actualizar" para ver datos más recientes

## Alertas y Notificaciones

El sistema muestra alertas en la parte superior:
- ✅ **Verde**: Operación exitosa
- ❌ **Rojo**: Error en la operación

Ejemplos:
- "Pipeline 'facebook_ads' ejecutado exitosamente. Filas procesadas: 150"
- "Configuración guardada exitosamente"
- "Error al ejecutar pipeline: Invalid access token"

## Tips y Mejores Prácticas

### Seguridad
- 🔒 **No compartas tu Access Token** - Es como una contraseña
- 🔄 **Renueva tokens periódicamente** - Los tokens expiran
- 🚫 **No subas credenciales a repositorios públicos**

### Performance
- ⏱️ **Primera sincronización tarda más** - Descarga todos los datos históricos
- 🔄 **Syncs subsecuentes son más rápidos** - Solo actualizan cambios
- 📊 **Insights requiere más tiempo** - Muchos datos de métricas

### Configuración
- 📅 **Ajusta date_range en insights** - Más días = más datos = más tiempo
- 📋 **Activa solo tablas necesarias** - Mejor performance
- ⚙️ **Guarda cambios antes de ejecutar** - Los cambios requieren guardar

## Solución de Problemas

### "Error: Invalid access token"
- Token expirado o inválido
- Generar nuevo token en Facebook Graph API Explorer
- Actualizar en configuración

### "Error: Cannot connect to MySQL"
- Verificar que MySQL esté corriendo: `docker-compose ps`
- Verificar credenciales en configuración de Destinos
- Si usas Docker, host debe ser `mysql` no `localhost`

### "No data extracted"
- Verificar que el Ad Account ID sea correcto
- Verificar permisos del token (necesita ads_read)
- Verificar que la cuenta tenga datos

### Tablas no aparecen en "Datos Sincronizados"
- Primero debes ejecutar un pipeline
- Las tablas se crean automáticamente en la primera sync
- Verificar logs: `docker-compose logs -f elt-api`

## Atajos de Teclado

- **Esc**: Cerrar modal abierto
- **F5**: Recargar página completa
- **Ctrl + R**: Recargar página

## Más Información

- **Ver logs en tiempo real**: `docker-compose logs -f elt-api`
- **Documentación API**: Ver endpoints en README.md
- **Configuración avanzada**: Editar `config/config.yaml`

---

**¿Necesitas ayuda?** Revisa los logs o abre un issue en GitHub.
