# 🎬 Tutorial Visual - Configuración de Insights

## Paso a Paso en Imágenes (Descripción)

### Pantalla 1: Interfaz Principal

```
╔════════════════════════════════════════════════════════════════╗
║                    🔄 Sistema ELT                              ║
║                Panel de Control y Configuración                ║
╚════════════════════════════════════════════════════════════════╝

[Desplázate hacia abajo...]
```

### Pantalla 2: Encontrar el Botón

Busca esta sección:

```
┌──────────────────────────────────────────────────────────────┐
│ 📋 Tablas Disponibles para Sincronizar                        │
│                                                              │
│ [📊 Configurar Insights]  [🔄 Actualizar]  ← Click aquí!   │
│                                                              │
│ campaigns               [🟢 ON]                              │
│ adsets                  [🟢 ON]                              │
│ ads                     [🟢 ON]                              │
│ insights                [🟢 ON]                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Pantalla 3: Modal Abierto

Click en "📊 Configurar Insights" abre este modal:

```
┌──────────────────────────────────────────────────────────────┐
│ 📊 Configuración de Insights                            [X] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Dimensión (Nivel de Agregación):                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ account                                             ▼  │ │
│  └────────────────────────────────────────────────────────┘ │
│  Opciones: account | campaign | adset | ad                  │
│                                                              │
│  Granularidad Temporal:                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ daily                                               ▼  │ │
│  └────────────────────────────────────────────────────────┘ │
│  Opciones: daily (diario) | monthly (mensual)              │
│                                                              │
│  Rango de Fechas:                                            │
│  Fecha Inicio: [________]  Fecha Fin: [________]            │
│  O                                                           │
│  Últimos días: [30]                                          │
│                                                              │
│  Métricas a Incluir:                                         │
│  ☑ Impresiones                                              │
│  ☑ Clics                                                    │
│  ☑ Gasto                                                    │
│  ☑ Alcance                                                  │
│  ☑ CTR (Tasa de Clics)                                      │
│  ☑ CPC (Costo por Clic)                                     │
│  ☑ CPM (Costo por Mil)                                      │
│  ☑ Frecuencia                                               │
│                                                              │
│  [💾 Guardar Configuración]  [Cancelar]                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Tutorial Interactivo

### Escenario 1: Cambiar a "Por Campaña"

**Paso 1**: Haz click en el selector Dimensión
```
Before:  ┌─────────────┐
         │ account  ▼ │
         └─────────────┘

After:   ┌─────────────────────────┐
         │ account          ▼     │
         │ campaign                │ ← Click aquí
         │ adset                   │
         │ ad                      │
         └─────────────────────────┘
```

**Paso 2**: Selecciona "campaign"
```
┌─────────────┐
│ campaign ▼ │  ← Ya seleccionado
└─────────────┘
```

**Paso 3**: Scroll hacia abajo y click "💾 Guardar"
```
[💾 Guardar Configuración]  ← Click
```

**Paso 4**: Espera la confirmación
```
┌─────────────────────────────────────────────────┐
│ ✅ Configuración de insights guardada           │
│    exitosamente                                 │
└─────────────────────────────────────────────────┘
```

---

### Escenario 2: Cambiar Rango de Fechas

**Paso 1**: Click en "Fecha Inicio"
```
Fecha Inicio: [2025-11-27] ← Click
```

**Paso 2**: Aparece calendario (navegador)
```
Selecciona: 2025-11-01
```

**Paso 3**: Click en "Fecha Fin"
```
Fecha Fin: [2025-11-30] ← Click
```

**Paso 4**: Selecciona última fecha de noviembre
```
Resultado:
Fecha Inicio: [2025-11-01]
Fecha Fin:    [2025-11-30]
```

**Paso 5**: Click "💾 Guardar"
```
✅ Guardado exitosamente
```

---

### Escenario 3: Seleccionar Solo Algunas Métricas

**Estado inicial**: Todas seleccionadas
```
☑ Impresiones
☑ Clics
☑ Gasto
☑ Alcance
☑ CTR
☑ CPC
☑ CPM
☑ Frecuencia
```

**Paso 1**: Deselecciona "Alcance"
```
Click en ☑ Alcance
↓
☐ Alcance  (Desseleccionado)
```

**Paso 2**: Deselecciona "Frecuencia"
```
Click en ☑ Frecuencia
↓
☐ Frecuencia  (Desseleccionado)
```

**Resultado**: Solo traerás
```
☑ Impresiones
☑ Clics
☑ Gasto
☑ CTR
☑ CPC
☑ CPM
```

**Paso 3**: Click "💾 Guardar"
```
✅ Guardado con 6 métricas
```

---

### Escenario 4: Configuración Completa - Análisis Semanal

**Objetivo**: Ver cada campaña con datos de la última semana

**Paso 1**: Cambiar Dimensión → "campaign"
```
Dimensión: [campaign ▼]
```

**Paso 2**: Mantener Granularidad → "daily"
```
Granularidad: [daily ▼]
```

**Paso 3**: Cambiar Últimos días → "7"
```
Últimos días: [7]  ← Cambiar de 30 a 7
```

**Paso 4**: Seleccionar métricas clave
```
Deseleccionar:
  ☐ Alcance
  ☐ CPM
  ☐ Frecuencia

Mantener:
  ☑ Impresiones
  ☑ Clics
  ☑ Gasto
  ☑ CTR
  ☑ CPC
```

**Paso 5**: Click "💾 Guardar"
```
┌────────────────────────────────────────┐
│ ✅ Configuración guardada exitosamente │
│    Modal cierra automáticamente        │
└────────────────────────────────────────┘
```

**Resultado en base de datos**:
```
date_start    campaign_name    campaign_id    impressions  clicks  spend
2025-11-21    Campaign A       111            1000         50      $10
2025-11-21    Campaign B       222            2000         100     $20
2025-11-22    Campaign A       111            1100         55      $11
2025-11-22    Campaign B       222            2100         105     $21
...           ...              ...            ...          ...     ...
2025-11-27    Campaign A       111            1500         75      $15
2025-11-27    Campaign B       222            2500         125     $25
```

---

## Videos (Si quisieras hacer un screencast)

### Video 1: Introducción (2 min)
```
00:00 - Mostrar interfaz principal
00:30 - Hacer click en "📊 Configurar Insights"
01:00 - Explicar qué es cada opción
01:30 - Demo: Cambiar dimensión
02:00 - Guardar y mostrar confirmación
```

### Video 2: Casos de Uso (5 min)
```
00:00 - Caso 1: Análisis por campaña
02:00 - Caso 2: Datos mensuales
04:00 - Caso 3: Seleccionar métricas
```

### Video 3: Integración (3 min)
```
00:00 - Cambiar configuración
00:30 - Ejecutar pipeline
01:00 - Mostrar datos nuevos en MySQL
02:00 - Explicar cómo se aplicaron cambios
```

---

## Animación de Cambio de Configuración

```
ANTES:
┌──────────────────────────┐
│ Dimensión: account       │
│ Días: 30                 │
│ Granularidad: daily      │
└──────────────────────────┘

(Click en Dimensión)
↓

┌──────────────────────────┐
│ Dimensión: campaign ◀── │ Cambio
│ Días: 30                 │
│ Granularidad: daily      │
└──────────────────────────┘

(Scroll, click Guardar)
↓

✅ Guardado
↓

PRÓXIMA SINCRONIZACIÓN:
└─→ Nueva data con "campaign"
```

---

## Consejos para Demostración

### Demo Exitosa
1. Comienza con valor por defecto (account)
2. Cambia a campaign
3. Muestra guardar
4. Ejecuta pipeline
5. Muestra datos nuevos en MySQL

### Timing
- Demo corta: 3 minutos
- Demo completa: 10 minutos
- Con preguntas: 15 minutos

### Puntos Clave a Enfatizar
1. ✨ Todo desde la web (sin editar archivos)
2. 🔄 Cambios inmediatos
3. 📊 Control completo sobre datos
4. 💾 Automáticamente guardado en config.yaml

---

## FAQ Mientras Demuestras

**P: ¿Se pierden datos si cambio?**
R: No, se agregan nuevos registros con la nueva configuración.

**P: ¿Cada cambio requiere re-sincronizar?**
R: La próxima sincronización automática usa los nuevos parámetros.

**P: ¿Puedo revertir cambios?**
R: Sí, simplemente vuelve a "Configurar Insights" y cambia.

**P: ¿Afecta a datos históricos?**
R: No, se mantienen. Se agregan nuevos según la configuración.

---

**Nota**: Este documento es una guía para hacer demos o tutoriales en video. Ajusta según tus necesidades.
