# 🚀 DEPLOYMENT GUIDE - RAILWAY

**Fecha de preparación**: 6 de Noviembre 2025  
**Estado**: ✅ LISTO PARA DEPLOY

---

## ✅ PREPARACIÓN COMPLETADA (HOY)

### Archivos Creados/Actualizados
- ✅ `.gitignore` - Actualizado con backups y logs
- ✅ `.env.example` - Template de variables de entorno
- ✅ `.env` - Configuración local (NO se sube a git)
- ✅ `requirements.txt` - Dependencias de producción
- ✅ `Procfile` - Configuración para Heroku/Railway
- ✅ `runtime.txt` - Python 3.13.0
- ✅ `settings.py` - SECRET_KEY, DEBUG, ALLOWED_HOSTS desde env
- ✅ WhiteNoise configurado para archivos estáticos
- ✅ `collectstatic` ejecutado exitosamente

### Limpieza
- ✅ Documentos viejos movidos a `docs/archive/planning/`
- ✅ `.gitignore` ignora backups y logs
- ✅ No hay credenciales hardcodeadas
- ✅ Variables de entorno configuradas

---

## 🚀 DEPLOYMENT MAÑANA (7 de Noviembre)

### Paso 1: Crear Cuenta en Railway (5 min)

1. Ve a https://railway.app
2. Sign up con GitHub
3. Autoriza Railway a acceder a tu repositorio

### Paso 2: Crear Proyecto (10 min)

#### Opción A: Desde GitHub (Recomendado)
```bash
# 1. Hacer commit de todos los cambios de hoy
git add .
git commit -m "feat: Preparar proyecto para deployment"
git push origin main

# 2. En Railway:
- Click "New Project"
- Seleccionar "Deploy from GitHub repo"
- Elegir "lino_saludable"
- Railway detectará Django automáticamente
```

#### Opción B: Desde CLI
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Iniciar proyecto
railway init

# Link a repo
railway link

# Deploy
railway up
```

### Paso 3: Configurar PostgreSQL (5 min)

1. En el dashboard de Railway:
   - Click "New" → "Database" → "PostgreSQL"
   - Railway crea automáticamente `DATABASE_URL`
   - No necesitas configurar nada más ✅

### Paso 4: Configurar Variables de Entorno (10 min)

En Railway Dashboard → Tu proyecto → Variables:

```bash
# REQUERIDAS
SECRET_KEY=<generar-nueva-key-super-segura>
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app

# AUTOMÁTICAS (Railway las crea)
DATABASE_URL=postgres://...  (ya configurada por Railway)
PORT=8000  (Railway la configura automáticamente)
```

**Para generar SECRET_KEY segura:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Paso 5: Deploy y Migrar (10 min)

Railway ejecutará automáticamente:
1. `pip install -r requirements.txt`
2. `python src/manage.py migrate` (desde Procfile)
3. `gunicorn lino_saludable.wsgi`

**Si algo falla, ver logs:**
```bash
railway logs
```

### Paso 6: Crear Superusuario (5 min)

```bash
# Opción A: Desde Railway CLI
railway run python src/manage.py createsuperuser

# Opción B: Desde dashboard
# Settings → Environment → Open Shell
python src/manage.py createsuperuser
```

Crear usuario:
- Username: admin
- Email: tu-email@gmail.com
- Password: <contraseña-segura>

### Paso 7: Poblar Datos Iniciales (15 min)

```bash
# Opción 1: Desde Railway shell
railway run python src/manage.py shell

# Luego ejecutar:
from gestion.models import *

# Crear materias primas
mp1 = MateriaPrima.objects.create(
    nombre="Avena Integral",
    unidad_medida='kg',
    stock_actual=10,
    stock_minimo=2,
    costo_unitario=850
)

# Crear productos
prod1 = Producto.objects.create(
    nombre="Avena 500gr",
    categoria='cereales',
    precio=1200,
    stock=20,
    stock_minimo=5,
    materia_prima_asociada=mp1,
    cantidad_fraccion=0.5,
    tipo_producto='reventa'
)

# ... más datos según necesites
```

**Opción 2: Usar script de población (recomendado)**
```bash
railway run python src/poblar_lino_real.py
```

### Paso 8: Testing en Producción (10 min)

1. Abrir tu app: `https://tu-app.railway.app`
2. Login con superusuario
3. Probar:
   - ✅ Dashboard carga correctamente
   - ✅ Crear materia prima
   - ✅ Crear producto
   - ✅ Crear compra
   - ✅ Crear venta
   - ✅ Ver rentabilidad
   - ✅ Ver reportes

### Paso 9: Configurar Dominio (Opcional - 15 min)

1. Comprar dominio (ej: www.linosaludable.com)
2. En Railway:
   - Settings → Domains → "Custom Domain"
   - Agregar tu dominio
   - Configurar DNS según instrucciones
3. Actualizar `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=linosaludable.com,www.linosaludable.com,tu-app.railway.app
   ```

---

## 🔐 SEGURIDAD POST-DEPLOYMENT

### 1. HTTPS Automático ✅
Railway configura SSL/TLS automáticamente.

### 2. Variables de Entorno Verificadas
- ✅ `SECRET_KEY` diferente al de desarrollo
- ✅ `DEBUG=False`
- ✅ `ALLOWED_HOSTS` solo tu dominio

### 3. Rate Limiting (Opcional)

**Si querés activar rate limiting:**

1. Agregar Redis en Railway:
   ```
   New → Database → Redis
   ```

2. Actualizar `settings.py`:
   ```python
   RATELIMIT_ENABLE = True
   
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': os.environ.get('REDIS_URL'),
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

3. Habilitar en INSTALLED_APPS:
   ```python
   'django_ratelimit',
   ```

---

## 📊 MONITOREO (Opcional pero Recomendado)

### Opción 1: Sentry (Errores)

1. Crear cuenta en https://sentry.io
2. Instalar:
   ```bash
   pip install sentry-sdk
   ```
3. Agregar a `requirements.txt`:
   ```
   sentry-sdk==1.40.0
   ```
4. Configurar en `settings.py`:
   ```python
   import sentry_sdk
   
   sentry_sdk.init(
       dsn=os.environ.get('SENTRY_DSN'),
       traces_sample_rate=1.0,
   )
   ```
5. Agregar variable en Railway:
   ```
   SENTRY_DSN=https://...@sentry.io/...
   ```

### Opción 2: Railway Logs

Ver logs en tiempo real:
```bash
railway logs --follow
```

---

## 💾 BACKUPS AUTOMÁTICOS

### Opción 1: Railway Backups (Recomendado)

Railway hace snapshots automáticos de PostgreSQL.

### Opción 2: Script de Backup Manual

Crear archivo `backup_db.sh`:
```bash
#!/bin/bash
railway run python src/manage.py dumpdata > backup_$(date +%Y%m%d).json
```

Ejecutar semanalmente:
```bash
chmod +x backup_db.sh
./backup_db.sh
```

---

## 🐛 TROUBLESHOOTING

### Error: "Application Error"
```bash
# Ver logs
railway logs

# Común: Falta variable de entorno
# Solución: Verificar SECRET_KEY, ALLOWED_HOSTS
```

### Error: "Static files not found"
```bash
# Ejecutar collectstatic manualmente
railway run python src/manage.py collectstatic --noinput
```

### Error: "Database connection failed"
```bash
# Verificar que PostgreSQL esté creado en Railway
# Settings → Database → PostgreSQL debe existir
```

### Error: "Module not found"
```bash
# Verificar requirements.txt
railway run pip list

# Reinstalar dependencias
railway run pip install -r requirements.txt
```

---

## 📋 CHECKLIST FINAL

### Pre-Deploy ✅
- ✅ Código en GitHub
- ✅ requirements.txt actualizado
- ✅ Procfile creado
- ✅ runtime.txt creado
- ✅ settings.py usa variables de entorno
- ✅ .gitignore actualizado
- ✅ collectstatic ejecutado

### Durante Deploy
- ⚠️ Cuenta Railway creada
- ⚠️ Proyecto conectado a GitHub
- ⚠️ PostgreSQL agregado
- ⚠️ Variables de entorno configuradas
- ⚠️ Deploy exitoso
- ⚠️ Migraciones aplicadas
- ⚠️ Superusuario creado

### Post-Deploy
- ⚠️ Testing completo
- ⚠️ Datos iniciales poblados
- ⚠️ Dominio configurado (opcional)
- ⚠️ Monitoreo activado (opcional)
- ⚠️ Backups configurados

---

## 🎯 TIEMPO ESTIMADO MAÑANA

- **Setup Railway**: 15-20 min
- **Configuración**: 15-20 min
- **Deploy y pruebas**: 20-30 min
- **Datos iniciales**: 15-20 min
- **Dominio (opcional)**: 15-20 min

**TOTAL**: 1-1.5 horas para tener el sistema en producción ✅

---

## 📞 CONTACTOS DE EMERGENCIA

### Railway Support
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Email: support@railway.app

### Django Docs
- Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Security: https://docs.djangoproject.com/en/5.2/topics/security/

---

**¡TODO LISTO PARA DEPLOYMENT MAÑANA! 🚀**

Siguiente paso: Descansar hoy, deploy mañana temprano.
