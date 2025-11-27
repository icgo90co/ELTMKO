-- Script de inicialización de la base de datos
-- Se ejecuta automáticamente cuando el contenedor MySQL se crea por primera vez

-- Crear base de datos si no existe (ya se crea con MYSQL_DATABASE)
-- CREATE DATABASE IF NOT EXISTS elt_data;

-- Usar la base de datos
USE elt_data;

-- Mensaje de confirmación
SELECT 'Base de datos inicializada correctamente' AS mensaje;
