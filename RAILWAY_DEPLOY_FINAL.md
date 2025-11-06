# 🚀 DESPLIEGUE RAILWAY - LINO SALUDABLE

## 📋 ARCHIVOS DE CONFIGURACIÓN (LIMPIADOS)

### ✅ Archivos Activos
- `railway.toml` - Configuración principal de Railway
- `nixpacks.toml` - Configuración de build Nixpacks
- `requirements.txt` - Dependencias Python
- `runtime.txt` - Versión Python (3.13.0)
- `.slugignore` - Archivos excluidos del build

### ❌ Archivos Eliminados (Conflictivos)
- ~~`Procfile`~~ - Railway prioriza railway.toml
- ~~`server.js`~~ - Archivo Node.js vacío innecesario
- ~~`package.json`~~ - Archivo Node.js vacío innecesario
- ~~`run_migrations_railway.py`~~ - Script temporal obsoleto
- ~~`migrate.sh`~~ - Script bash redundante
- ~~`start.sh`~~ - Script bash redundante
- ~~`src/test_*.py`~~ - Scripts de testing (no necesarios en producción)
- ~~`src/check_*.py`~~ - Scripts de debug
- ~~`src/cleanup_*.py`~~ - Scripts temporales

## 🔧 CONFIGURACIÓN ACTUAL

### railway.toml
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "cd src && python manage.py migrate --noinput --verbosity 2 && python manage.py createusers && gunicorn lino_saludable.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --log-file - --access-logfile - --error-logfile - --log-level info"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### nixpacks.toml
```toml
[phases.setup]
nixPkgs = ["python313", "postgresql"]

[phases.install]
cmds = [
    "pip install --upgrade pip setuptools wheel",
    "pip install -r requirements.txt"
]

[phases.build]
cmds = [
    "cd src && python manage.py collectstatic --noinput --clear"
]

[start]
cmd = "cd src && python manage.py migrate --noinput --verbosity 2 && python manage.py createusers && gunicorn lino_saludable.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 60 --log-file -"
```

## 🌐 VARIABLES DE ENTORNO RAILWAY

Asegúrate de tener configuradas:

```bash
DATABASE_URL=postgresql://postgres:***@postgres.railway.internal:5432/railway
SECRET_KEY=<tu-secret-key-aqui>
DEBUG=false
ALLOWED_HOSTS=web-production-b0ad1.up.railway.app,*.railway.app
ADMIN_PASSWORD_1=<contraseña-segura-1>  # Opcional, usa default si no está
ADMIN_PASSWORD_2=<contraseña-segura-2>  # Opcional, usa default si no está
```

## 📝 PASOS PARA REDESPLEGAR

1. **Commit y Push**
   ```bash
   git add .
   git commit -m "🧹 Limpieza de archivos y optimización Railway"
   git push origin main
   ```

2. **Railway Auto-Deploy**
   - Railway detectará el push y redesplegará automáticamente
   - Monitorea los logs en: https://railway.app/project/<tu-proyecto>/service/web

3. **Verificar Deploy Logs**
   Deberías ver:
   ```
   [BUILD] Collecting static files...
   [DEPLOY] Running migrations...
   [DEPLOY] Operations to perform:
   [DEPLOY] Creating users...
   [DEPLOY] ✅ Usuario sister_emprendedora creado
   [DEPLOY] ✅ Usuario el_super_creador creado
   [DEPLOY] Starting gunicorn...
   ```

4. **Verificar Aplicación**
   - URL: https://web-production-b0ad1.up.railway.app/admin/
   - Login con: `sister_emprendedora` o `el_super_creador`
   - Contraseñas: Ver variables de entorno o defaults

## 🛠️ TROUBLESHOOTING

### Si las migraciones no se ejecutan:

1. **Verificar railway.toml está siendo usado**
   - Logs deben mostrar el comando completo con `migrate`

2. **Forzar ejecución manual** (última opción)
   ```bash
   railway shell --service web
   cd src && python manage.py migrate --noinput
   python manage.py createusers
   exit
   ```

3. **Revisar logs de PostgreSQL**
   ```bash
   railway logs --service postgres
   ```

### Si hay errores de conexión DB:

1. Verificar `DATABASE_URL` en variables de entorno
2. Verificar servicio PostgreSQL está corriendo
3. Verificar link entre servicios web <-> postgres

## 📊 ESTRUCTURA FINAL DEL PROYECTO

```
/
├── railway.toml           ← Configuración principal Railway
├── nixpacks.toml          ← Build configuration
├── requirements.txt       ← Python dependencies
├── runtime.txt            ← Python version
├── .slugignore           ← Archivos excluidos del build
├── .gitignore            ← Git ignore
└── src/
    ├── manage.py
    ├── lino_saludable/
    │   ├── settings.py
    │   └── wsgi.py
    └── gestion/
        └── management/
            └── commands/
                └── createusers.py  ← Comando mejorado
```

## ✅ CHECKLIST FINAL

- [x] Archivos conflictivos eliminados
- [x] railway.toml configurado correctamente
- [x] nixpacks.toml simplificado
- [x] .slugignore creado
- [x] createusers.py mejorado con variables de entorno
- [x] Scripts de testing eliminados de src/
- [ ] Variables de entorno configuradas en Railway
- [ ] Commit y push realizados
- [ ] Deploy exitoso verificado
- [ ] Login en /admin/ funcional
- [ ] Contraseñas cambiadas

## 🎯 PRÓXIMOS PASOS

1. **Commit los cambios**
2. **Push a GitHub**
3. **Esperar auto-deploy de Railway**
4. **Verificar logs**
5. **Acceder a /admin/**
6. **¡CAMBIAR CONTRASEÑAS INMEDIATAMENTE!**

---

**Fecha de limpieza:** 6 de noviembre de 2025  
**Estado:** ✅ Proyecto limpio y optimizado para Railway
