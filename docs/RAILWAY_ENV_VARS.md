# 🔐 VARIABLES DE ENTORNO PARA RAILWAY

**Fecha**: 6 Nov 2025  
**Para**: Configurar en Railway después del primer deploy

---

## 📋 VARIABLES REQUERIDAS

Copiá y pegá estas variables en Railway → Settings → Variables

### 1. SECRET_KEY
```
SECRET_KEY=thr=+nrkmr5z85me*)038+bx+m^af0akyw8ba&(d@ly)q9&=n=
```
**Importante**: Esta key es ÚNICA para producción. NO uses la de desarrollo.

### 2. DEBUG
```
DEBUG=False
```
**Importante**: Debe estar en False en producción.

### 3. ALLOWED_HOSTS
```
ALLOWED_HOSTS=web-production-b0ad1.up.railway.app
```
**Importante**: Reemplazá con tu URL real de Railway (la que te dé Railway).

### 4. DJANGO_SETTINGS_MODULE (Opcional)
```
DJANGO_SETTINGS_MODULE=lino_saludable.settings
```

---

## 🗄️ DATABASE_URL

**NO NECESITAS CONFIGURARLA MANUALMENTE**

Railway la crea automáticamente cuando agregás PostgreSQL:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## 📝 CÓMO AGREGAR VARIABLES EN RAILWAY

1. En Railway → Tu proyecto "web"
2. Click en **"Variables"** (pestaña superior)
3. Click **"+ New Variable"**
4. Nombre: `SECRET_KEY`
5. Valor: `thr=+nrkmr5z85me*)038+bx+m^af0akyw8ba&(d@ly)q9&=n=`
6. Click **"Add"**
7. Repetir para `DEBUG` y `ALLOWED_HOSTS`

---

## ⚠️ ORDEN RECOMENDADO

1. ✅ Esperar que termine el deploy actual
2. ✅ Agregar PostgreSQL database
3. ✅ Agregar variables de entorno
4. ✅ Railway hace re-deploy automático
5. ✅ ¡Funciona! 🎉

---

## 🔄 DESPUÉS DE AGREGAR VARIABLES

Railway va a hacer **re-deploy automático**. Esperá 2-3 minutos y el sitio debería estar funcionando.

---

**SIGUIENTE PASO**: Cuando el deploy actual termine (puede fallar, es OK), agregamos PostgreSQL.
