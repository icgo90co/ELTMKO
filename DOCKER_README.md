# 🚀 Inicio Rápido con Docker

## 1. Verificar sistema
```bash
./docker-verify.sh
```

## 2. Configurar credenciales
```bash
# Editar .env con tus credenciales de Facebook Ads
nano .env
```

## 3. Iniciar sistema
```bash
./docker-start.sh
```

## 4. Acceder
Abrir en navegador: **http://localhost:5000**

---

## Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Detener
./docker-stop.sh

# Ejecutar pipeline
./docker-run-pipeline.sh

# Estado
docker-compose ps

# Reiniciar
docker-compose restart
```

## Ayuda completa
- Docker completo: `docs/DOCKER.md`
- README principal: `README.md`
- Quick start: `DOCKER_QUICKSTART.md`
