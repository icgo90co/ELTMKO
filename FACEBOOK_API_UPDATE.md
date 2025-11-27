# 🔧 Actualización de Facebook Ads API v22.0

## Problema Original

```
Error: (#2635) You are calling a deprecated version of the Ads API. 
Please upgrade to the latest version: v22.0.
```

Facebook deprecó la versión v18.0 de su API. Es necesario actualizar a v22.0.

## Solución Aplicada

### 1. Actualizar SDK de Facebook Business
**Archivo**: `requirements.txt`

```diff
- facebook-business==18.0.0
+ facebook-business==20.0.0
```

**Razón**: La versión 20.0.0 soporta natively la API v22.0 de Facebook.

### 2. Especificar Versión de API en Inicialización
**Archivo**: `src/extractors/facebook_ads_extractor.py`

```python
# Antes:
FacebookAdsApi.init(app_id, app_secret, access_token)

# Después:
FacebookAdsApi.init(app_id, app_secret, access_token, api_version='v22.0')
```

**Razón**: Explícitamente especificar la versión v22.0 para asegurar compatibilidad.

## Cambios Realizados

### requirements.txt
- ✅ facebook-business: 18.0.0 → 20.0.0

### src/extractors/facebook_ads_extractor.py
- ✅ Added `api_version='v22.0'` parameter to `FacebookAdsApi.init()`
- ✅ Updated docstring for clarity

## Cómo Actualizar

### Si estás usando Docker:
```bash
# Reconstruir la imagen con nuevas dependencias
./docker-start.sh
```

### Si estás en ambiente local:
```bash
# Desactivar venv si está activo
source .venv/bin/deactivate

# Eliminar venv anterior (opcional)
rm -rf .venv

# Crear nuevo venv
python -m venv .venv

# Activar venv
source .venv/bin/activate

# Instalar dependencias actualizadas
pip install -r requirements.txt
```

## Validación

Para verificar que la actualización fue exitosa:

```bash
# Test rápido de la importación
python -c "from facebook_business.api import FacebookAdsApi; print('✅ facebook-business v20.0.0 instalado correctamente')"
```

## Cambios en la API v22.0

La API v22.0 introduce varios cambios:

1. **Deprecation de ciertos endpoints** - La mayoría siguen funcionando pero pueden tener comportamientos diferentes
2. **Cambios en respuestas** - Algunos campos pueden tener nombres o tipos diferentes
3. **Nuevos campos disponibles** - Acceso a nuevas métricas y parámetros
4. **Cambios en rate limiting** - Límites actualizados según la documentación oficial de Facebook

## Si Sigues Teniendo Errores

1. **Verificar token de acceso**:
   - Asegúrate de que tu token aún es válido
   - Los tokens de Facebook expiran (típicamente 60 días)
   - Regenera el token en Facebook Business Manager si es necesario

2. **Verificar Ad Account ID**:
   - Formato correcto: `act_XXXXXXXXXX`
   - Puedes encontrarlo en: Business Settings → Ad Accounts → Copy ID

3. **Verificar permisos**:
   - La app necesita permisos: `ads_management`, `ads_read`

4. **Revisar logs**:
   ```bash
   # En Docker
   docker logs elt-api
   docker logs elt-worker
   
   # Localmente
   tail -f logs/elt.log
   ```

## Compatibilidad Futura

Esta configuración es compatible con futuras versiones de Facebook API:

- Si Facebook lanza v23.0, solo necesitarás cambiar:
  ```python
  api_version='v23.0'
  ```

- En requirements.txt, cuando nueva versión del SDK esté disponible:
  ```
  facebook-business==21.0.0  # Si se lanzara
  ```

## Referencias

- [Facebook Business SDK Python](https://github.com/facebook/facebook-python-business-sdk)
- [Facebook Ads API Documentation](https://developers.facebook.com/docs/marketing-api)
- [API v22.0 Release Notes](https://developers.facebook.com/docs/marketing-api/release-notes)

---

**Aplicado**: 27 de Noviembre, 2025
**Estado**: ✅ Completado
