# 📚 Índice de Documentación - Sistema ELT

## 🚀 Inicio Rápido

- **[DOCKER_README.md](DOCKER_README.md)** - Comandos esenciales (1 página)
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** - Guía de inicio rápido (5 min)

## 📖 Documentación Principal

- **[README.md](README.md)** - Documentación general del sistema
- **[docs/DOCKER.md](docs/DOCKER.md)** - Guía completa de Docker
- **[WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)** - Guía de la interfaz web

## 📊 Configuración de Insights (Nuevo!)

- **[INSIGHTS_README.md](INSIGHTS_README.md)** - Comienza aquí! Guía de inicio rápido
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Resumen de 1 página
- **[INSIGHTS_EXECUTIVE_SUMMARY.md](INSIGHTS_EXECUTIVE_SUMMARY.md)** - Para no-técnicos
- **[INSIGHTS_CONFIGURATION_GUIDE.md](INSIGHTS_CONFIGURATION_GUIDE.md)** - Guía completa de configuración
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Cómo probar todas las funciones
- **[INSIGHTS_CHANGES_SUMMARY.md](INSIGHTS_CHANGES_SUMMARY.md)** - Cambios técnicos realizados
- **[VISUAL_TUTORIAL.md](VISUAL_TUTORIAL.md)** - Tutorial visual con imágenes ASCII
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Resumen técnico de implementación
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Resumen ejecutivo
- **[VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md)** - Checklist de validación

## 🔧 Referencias Técnicas

- **[DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)** - Resumen de implementación Docker
- **[DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md)** - Comandos útiles de Docker
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía de despliegue en producción

## 💡 Ejemplos

- **[examples/README.md](examples/README.md)** - Ejemplos de uso
- **[examples/usage_examples.py](examples/usage_examples.py)** - Código de ejemplo

## 📋 Por Caso de Uso

### ¿Primera vez usando el sistema?
1. Lee [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
2. Ejecuta `./docker-verify.sh`
3. Ejecuta `./docker-start.sh`
4. Abre http://localhost:5000 y lee [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md)

### ¿Quieres entender la arquitectura?
1. Lee [DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)
2. Revisa [README.md](README.md)

### ¿Necesitas comandos específicos?
- Consulta [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md)
- O ejecuta `make help`

### ¿Vas a desplegar en producción?
1. Lee [DEPLOYMENT.md](DEPLOYMENT.md)
2. Revisa [docs/DOCKER.md](docs/DOCKER.md) sección de producción

### ¿Quieres extender el sistema?
1. Lee [README.md](README.md) sección "Agregar Nuevos Conectores"
2. Revisa [examples/usage_examples.py](examples/usage_examples.py)

### ¿Tienes un problema?
1. Revisa [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) sección "Troubleshooting"
2. Consulta [docs/DOCKER.md](docs/DOCKER.md) sección "Troubleshooting"
3. Ejecuta `docker-compose logs`

## 📁 Estructura de Archivos

```
ELTMKO/
├── README.md                    # 📖 Documentación principal
├── DOCKER_README.md             # 🚀 Inicio rápido Docker
├── DOCKER_QUICKSTART.md         # ⚡ Guía 5 minutos
├── DOCKER_SUMMARY.md            # 📊 Resumen implementación
├── DOCKER_CHEATSHEET.md         # 📋 Comandos útiles
├── DEPLOYMENT.md                # 🚀 Despliegue producción
├── docs/
│   └── DOCKER.md               # 📖 Guía completa Docker
└── examples/
    ├── README.md               # 💡 Guía de ejemplos
    └── usage_examples.py       # 🐍 Código de ejemplo
```

## 🔍 Búsqueda Rápida

| Necesito... | Documento |
|-------------|-----------|
| Iniciar el sistema | [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) |
| Usar la interfaz web | [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) |
| Configurar Insights | [INSIGHTS_EXECUTIVE_SUMMARY.md](INSIGHTS_EXECUTIVE_SUMMARY.md) |
| Entender Insights en detalle | [INSIGHTS_CONFIGURATION_GUIDE.md](INSIGHTS_CONFIGURATION_GUIDE.md) |
| Probar nueva funcionalidad | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Ver cambios técnicos | [INSIGHTS_CHANGES_SUMMARY.md](INSIGHTS_CHANGES_SUMMARY.md) |
| Ver comandos Docker | [DOCKER_CHEATSHEET.md](DOCKER_CHEATSHEET.md) |
| Entender arquitectura | [DOCKER_SUMMARY.md](DOCKER_SUMMARY.md) |
| Desplegar en servidor | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Configurar pipelines | [README.md](README.md) |
| Solucionar problemas | [docs/DOCKER.md](docs/DOCKER.md) |
| Ver ejemplos de código | [examples/usage_examples.py](examples/usage_examples.py) |
| Agregar conector | [README.md](README.md) + [examples/](examples/) |

## 🎯 Guías por Nivel

### Nivel Principiante
1. [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)
2. [DOCKER_README.md](DOCKER_README.md)
3. Interfaz web (http://localhost:5000)

### Nivel Intermedio
1. [README.md](README.md)
2. [DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)
3. [examples/usage_examples.py](examples/usage_examples.py)

### Nivel Avanzado
1. [docs/DOCKER.md](docs/DOCKER.md)
2. [DEPLOYMENT.md](DEPLOYMENT.md)
3. Código fuente en `src/`

## 📞 Soporte

- **Documentación**: Revisa los archivos arriba
- **Logs**: `docker-compose logs -f`
- **Verificación**: `./docker-verify.sh`
- **Issues**: GitHub Issues del proyecto

---

**Tip**: Usa `Ctrl+F` en los documentos para búsqueda rápida de palabras clave.
