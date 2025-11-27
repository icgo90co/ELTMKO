################################################################################
# Makefile para simplificar comandos Docker
################################################################################

.PHONY: help build up down restart logs clean dev test

# Configuración
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_DEV := docker-compose -f docker-compose.dev.yml

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Producción
build: ## Construir imágenes Docker
	$(DOCKER_COMPOSE) build

up: ## Iniciar servicios
	$(DOCKER_COMPOSE) up -d mysql elt-api

up-all: ## Iniciar todos los servicios (incluyendo worker)
	$(DOCKER_COMPOSE) --profile worker up -d

down: ## Detener servicios
	$(DOCKER_COMPOSE) down

restart: ## Reiniciar servicios
	$(DOCKER_COMPOSE) restart

logs: ## Ver logs
	$(DOCKER_COMPOSE) logs -f

logs-api: ## Ver logs de API
	$(DOCKER_COMPOSE) logs -f elt-api

logs-mysql: ## Ver logs de MySQL
	$(DOCKER_COMPOSE) logs -f mysql

status: ## Ver estado de contenedores
	$(DOCKER_COMPOSE) ps

clean: ## Limpiar contenedores y volúmenes
	$(DOCKER_COMPOSE) down -v

run-pipeline: ## Ejecutar pipeline manualmente
	$(DOCKER_COMPOSE) run --rm elt-api python main.py --mode once

shell-api: ## Shell interactivo en contenedor API
	$(DOCKER_COMPOSE) exec elt-api bash

shell-mysql: ## Shell MySQL
	$(DOCKER_COMPOSE) exec mysql mysql -u eltuser -peltpassword elt_data

# Desarrollo
dev-build: ## Construir imágenes de desarrollo
	$(DOCKER_COMPOSE_DEV) build

dev-up: ## Iniciar en modo desarrollo
	$(DOCKER_COMPOSE_DEV) up

dev-down: ## Detener desarrollo
	$(DOCKER_COMPOSE_DEV) down

dev-logs: ## Ver logs en desarrollo
	$(DOCKER_COMPOSE_DEV) logs -f

# Utilidades
prune: ## Limpiar todo Docker (⚠️ cuidado)
	docker system prune -a --volumes

backup-db: ## Hacer backup de MySQL
	docker-compose exec -T mysql mysqldump -u eltuser -peltpassword elt_data > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restaurar backup (usar: make restore-db FILE=backup.sql)
	docker-compose exec -T mysql mysql -u eltuser -peltpassword elt_data < $(FILE)

install: ## Instalación completa
	@echo "🐳 Instalando Sistema ELT..."
	@if [ ! -f .env ]; then cp .env.docker .env; echo "✅ Archivo .env creado"; fi
	@mkdir -p logs
	@echo "✅ Directorios creados"
	@$(DOCKER_COMPOSE) build
	@echo "✅ Imágenes construidas"
	@$(DOCKER_COMPOSE) up -d mysql elt-api
	@echo "⏳ Esperando MySQL..."
	@sleep 10
	@echo "✅ Sistema iniciado en http://localhost:5000"

.DEFAULT_GOAL := help
