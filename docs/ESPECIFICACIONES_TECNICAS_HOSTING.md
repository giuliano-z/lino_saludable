# 📋 ESPECIFICACIONES TÉCNICAS - LINO SALUDABLE

**Proyecto**: Sistema de Gestión para Dietética  
**Versión**: 1.0.0  
**Fecha**: 6 de Noviembre 2025  
**Propósito**: Buscar opciones de hosting/servidor en la nube

---

## 🖥️ STACK TECNOLÓGICO

### Backend
- **Framework**: Django 5.2.4
- **Lenguaje**: Python 3.13.0
- **WSGI Server**: Gunicorn 23.0.0
- **Base de Datos (Desarrollo)**: SQLite3
- **Base de Datos (Producción)**: PostgreSQL (cualquier versión >= 12)

### Frontend
- **Template Engine**: Django Templates (Jinja2-like)
- **CSS**: Custom CSS (sin framework, archivos estáticos)
- **JavaScript**: Vanilla JS (sin frameworks)
- **Archivos Estáticos**: 168 archivos (~5 MB total)

### Dependencias Python Completas
```
asgiref==3.8.1
Django==5.2.4
django-extensions==3.2.3
django-ratelimit==4.1.0
django-redis==6.0.0
gunicorn==23.0.0
packaging==25.0
psycopg2-binary==2.9.11
python-dotenv==1.2.1
redis==7.0.1
sqlparse==0.5.3
whitenoise==6.11.0
```

---

## 💾 REQUISITOS DE INFRAESTRUCTURA

### Servidor de Aplicación
- **RAM Mínima**: 512 MB (recomendado 1 GB)
- **CPU**: 1 vCPU (shared OK para empezar)
- **Almacenamiento**: 1 GB mínimo (2 GB recomendado)
- **Sistema Operativo**: Linux (Ubuntu 20.04/22.04, Debian, etc.)
- **Python**: 3.11+ (3.13 ideal)

### Base de Datos
- **Motor**: PostgreSQL 12+ o MySQL 8+
- **Almacenamiento DB**: 500 MB inicial (crece con uso)
- **Conexiones**: 10-20 conexiones simultáneas
- **Backups**: Diarios recomendados

### Archivos Estáticos
- **Espacio**: 10-20 MB
- **CDN**: Opcional pero recomendado
- **Storage**: Filesystem o S3-compatible

### Networking
- **Ancho de Banda**: 10 GB/mes mínimo
- **Tráfico Estimado**: 
  - ~50-100 requests/día (inicio)
  - ~1000-2000 requests/día (uso normal)
- **SSL/HTTPS**: REQUERIDO

---

## 📁 ESTRUCTURA DEL PROYECTO

### Directorios Importantes
```
lino_saludable/
├── src/                           → Código principal
│   ├── manage.py                  → Django management
│   ├── lino_saludable/            → Settings del proyecto
│   │   ├── settings.py            → Configuración principal
│   │   ├── urls.py                → Rutas
│   │   └── wsgi.py                → WSGI application
│   ├── gestion/                   → App principal
│   │   ├── models.py              → 12 modelos de base de datos
│   │   ├── views.py               → Lógica de negocio
│   │   ├── templates/             → HTML templates
│   │   └── static/                → CSS, JS, imágenes
│   └── static/                    → Archivos estáticos globales
├── requirements.txt               → Dependencias Python
├── Procfile                       → Comando de inicio (opcional)
├── runtime.txt                    → Python 3.13.0
└── .env                           → Variables de entorno (NO subir)
```

### Archivos de Configuración
- **Procfile**: `web: gunicorn lino_saludable.wsgi --log-file -`
- **runtime.txt**: `python-3.13.0`
- **requirements.txt**: 12 paquetes Python

---

## ⚙️ VARIABLES DE ENTORNO REQUERIDAS

### Esenciales (SIEMPRE)
```bash
SECRET_KEY=<string-aleatorio-50-caracteres>
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

### Opcionales
```bash
# Redis (para caché/rate limiting)
REDIS_URL=redis://localhost:6379/0

# Email (notificaciones futuras)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app

# Sentry (monitoreo errores)
SENTRY_DSN=https://...@sentry.io/...
```

---

## 🗄️ BASE DE DATOS

### Esquema
- **12 Modelos/Tablas**:
  1. `MateriaPrima` (ingredientes, stock)
  2. `Producto` (productos finales)
  3. `Receta` (composición productos elaborados)
  4. `ItemReceta` (ingredientes de cada receta)
  5. `Compra` (compras de materias primas)
  6. `ItemCompra` (detalle de compras)
  7. `Venta` (ventas realizadas)
  8. `ItemVenta` (detalle de ventas)
  9. `Produccion` (lotes producidos)
  10. `User` (Django auth)
  11. `Session` (Django sessions)
  12. `ContentType`, `Permission`, etc. (Django internals)

### Migraciones
- **18 archivos** de migración en `gestion/migrations/`
- **Comando inicial**: `python manage.py migrate`

### Datos Iniciales
- Script de población: `src/poblar_lino_real.py`
- Crea ~10-15 registros de ejemplo

---

## 🚀 COMANDOS DE DEPLOYMENT

### 1. Instalación
```bash
# Clonar repo
git clone https://github.com/giuliano-z/lino_saludable.git
cd lino_saludable

# Crear entorno virtual
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración
```bash
# Copiar variables de entorno
cp .env.example .env
# Editar .env con valores reales

# Colectar archivos estáticos
cd src
python manage.py collectstatic --noinput
```

### 3. Base de Datos
```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Poblar datos de prueba (opcional)
python poblar_lino_real.py
```

### 4. Ejecutar
```bash
# Desarrollo
python manage.py runserver 0.0.0.0:8000

# Producción
gunicorn lino_saludable.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

---

## 🔐 REQUISITOS DE SEGURIDAD

### SSL/TLS
- **Obligatorio**: HTTPS en producción
- **Redirect**: HTTP → HTTPS automático
- **HSTS**: Configurado en settings.py

### Autenticación
- Django Auth integrado
- Login requerido para todas las vistas
- Session-based authentication

### CORS
- No requiere CORS (no es API pública)
- Solo web tradicional (server-side rendering)

### Rate Limiting
- Configurado con `django-ratelimit`
- Límites actuales: 100 requests/hora por IP

---

## 📊 CARACTERÍSTICAS DEL SISTEMA

### Funcionalidades Principales
1. **Gestión de Inventario**
   - Materias primas
   - Productos (reventa y elaborados)
   - Control de stock
   - Alertas stock mínimo

2. **Compras**
   - Registro de compras
   - Actualización automática de stock
   - Cálculo de costos

3. **Ventas**
   - Registro de ventas
   - Descuento automático de stock
   - Cálculo de ingresos

4. **Producción**
   - Recetas de productos elaborados
   - Control de lotes producidos
   - Cálculo de costos de producción

5. **Dashboards**
   - Dashboard general (KPIs)
   - Dashboard de inventario
   - Dashboard de rentabilidad
   - Reportes visuales

### Performance Actual
- **Tests completados**: 8/8 ✅
- **Tiempo de carga**: <500ms (localhost)
- **Usuarios simultáneos**: Testeado con 1 (escala a 10-20)

---

## 🌐 OPCIONES DE HOSTING EVALUADAS

### Características Deseadas
✅ **Debe tener**:
- Python 3.11+ support
- PostgreSQL incluido o fácil de agregar
- SSL/HTTPS automático
- Deploy desde Git
- Logs accesibles
- Backups automáticos

🎯 **Nice to have**:
- Free tier o bajo costo (<$10/mes)
- Auto-scaling
- Monitoreo incluido
- CLI para management
- Soporte en español

### Presupuesto
- **Ideal**: Gratis o <$5/mes
- **Aceptable**: $5-15/mes
- **Máximo**: $20/mes

---

## 📈 PROYECCIÓN DE CRECIMIENTO

### Fase 1 (Primeros 3 meses)
- 1-2 usuarios concurrentes
- ~50 requests/día
- Database: <100 MB
- Tráfico: <5 GB/mes

### Fase 2 (6-12 meses)
- 5-10 usuarios concurrentes
- ~500 requests/día
- Database: 200-500 MB
- Tráfico: 20-50 GB/mes

### Fase 3 (1+ año)
- 10-20 usuarios concurrentes
- ~2000 requests/día
- Database: 1-2 GB
- Tráfico: 100+ GB/mes

---

## 🛠️ INTEGRACIONES ACTUALES

### Servicios Externos
- **Ninguno** actualmente (100% self-contained)

### Servicios Opcionales Futuros
- Sentry (monitoreo de errores)
- SendGrid/Mailgun (emails)
- Redis (caché)
- S3/Cloudflare (CDN para estáticos)

---

## 🔍 PREGUNTAS PARA HACER A OTROS ASESORES

### Sobre la Plataforma
1. ¿Soporta Python 3.13? (o mínimo 3.11)
2. ¿PostgreSQL incluido o debo contratar separado?
3. ¿SSL/HTTPS incluido?
4. ¿Cómo es el proceso de deploy? (Git, FTP, CLI)
5. ¿Hay free tier o período de prueba?
6. ¿Cuánto cuesta después del free tier?

### Sobre Configuración
7. ¿Cómo se configuran variables de entorno?
8. ¿Ejecuta `collectstatic` automáticamente?
9. ¿Ejecuta migraciones automáticamente?
10. ¿Cómo accedo a los logs?
11. ¿Hay shell/SSH para debugging?
12. ¿Soporta `gunicorn` o usa otro WSGI server?

### Sobre Escalabilidad
13. ¿Cuántos requests/día soporta el plan básico?
14. ¿Cuánta RAM/CPU tengo?
15. ¿Hay límites de base de datos?
16. ¿Puedo escalar fácilmente si crece?

### Sobre Backups y Seguridad
17. ¿Backups automáticos de base de datos?
18. ¿Con qué frecuencia?
19. ¿Puedo restaurar fácilmente?
20. ¿Monitoreo de uptime incluido?

### Sobre Soporte
21. ¿Hay documentación en español?
22. ¿Soporte técnico? ¿Por qué canal?
23. ¿Comunidad activa?
24. ¿Tutoriales para Django?

---

## 📦 ALTERNATIVAS A RAILWAY

### PaaS (Platform as a Service)
1. **Railway** (mi recomendación original)
   - Pros: Simple, $5 gratis, PostgreSQL incluido
   - Contras: Después de créditos ~$10-15/mes

2. **Heroku**
   - Pros: Muy conocido, buena documentación
   - Contras: Ya no hay free tier, ~$7-13/mes

3. **Render**
   - Pros: Free tier existe, PostgreSQL gratis
   - Contras: Free tier duerme después de inactividad

4. **PythonAnywhere**
   - Pros: Especializado en Python, $5/mes
   - Contras: Configuración manual, menos automático

5. **Fly.io**
   - Pros: Free tier generoso, global
   - Contras: Curva de aprendizaje más alta

6. **Digital Ocean App Platform**
   - Pros: $5/mes, PostgreSQL incluido
   - Contras: Puede ser complejo para principiantes

### VPS (Más control, más trabajo)
7. **Digital Ocean Droplet**
   - Pros: $6/mes, control total
   - Contras: Debes configurar TODO (Nginx, SSL, etc.)

8. **Linode/Akamai**
   - Pros: $5/mes, buenos tutoriales
   - Contras: Configuración manual

9. **Vultr**
   - Pros: Desde $2.50/mes
   - Contras: Debes ser sysadmin

### Serverless (Experimental)
10. **Vercel** (con adaptaciones)
    - Pros: Deploy super rápido
    - Contras: Django no es ideal para serverless

---

## 📄 ARCHIVOS PARA COMPARTIR

Si otro asesor necesita ver código, estos son los archivos clave:

### Configuración
- `requirements.txt` - Dependencias
- `Procfile` - Comando de inicio
- `runtime.txt` - Versión Python
- `.env.example` - Variables necesarias

### Django Settings
- `src/lino_saludable/settings.py` - Configuración completa
- `src/lino_saludable/wsgi.py` - WSGI application

### Modelos
- `src/gestion/models.py` - Estructura de base de datos

### Documentación
- `docs/PRODUCTION_READY.md` - Estado del proyecto
- `docs/deployment/RAILWAY_DEPLOYMENT_GUIDE.md` - Guía de deploy

---

## ✅ ESTADO ACTUAL

### ¿Qué está listo?
- ✅ Código funcional y testeado (8/8 tests)
- ✅ Variables de entorno configuradas
- ✅ WhiteNoise para archivos estáticos
- ✅ Gunicorn configurado
- ✅ PostgreSQL-ready (usando `psycopg2-binary`)
- ✅ Migraciones creadas
- ✅ .gitignore configurado
- ✅ Secret key en variable de entorno

### ¿Qué falta?
- ⚠️ Elegir plataforma de hosting
- ⚠️ Crear cuenta en la plataforma
- ⚠️ Hacer deploy
- ⚠️ Configurar dominio (opcional)

---

## 🎯 CRITERIOS DE DECISIÓN

### Prioridad Alta
1. **Simplicidad** - Que sea fácil hacer deploy
2. **Costo** - Gratis o <$10/mes para empezar
3. **PostgreSQL** - Incluido o fácil de agregar
4. **SSL** - Automático
5. **Logs** - Accesibles y claros

### Prioridad Media
6. **Documentación** - En español o muy clara
7. **Backups** - Automáticos
8. **Escalabilidad** - Fácil crecer
9. **Soporte** - Comunidad o support técnico

### Prioridad Baja
10. **Auto-scaling** - No crítico ahora
11. **CDN** - Puede agregarse después
12. **Monitoreo** - Podemos usar Sentry aparte

---

## 📞 INFORMACIÓN DE CONTACTO DEL PROYECTO

- **GitHub**: https://github.com/giuliano-z/lino_saludable
- **Desarrollador**: Giuliano Zulatto
- **Propósito**: Sistema de gestión para dietética
- **Usuarios objetivo**: 1-10 (pequeño negocio)
- **Región**: Argentina (latencia LATAM importante)

---

## 🚨 PREGUNTAS URGENTES

Si vas a consultar con otro asesor, preguntale:

1. **¿Cuál es la opción MÁS SIMPLE para un Django project como este?**
2. **¿Cuánto me va a costar realmente por mes?** (sin sorpresas)
3. **¿Cuánto tarda el primer deploy?** (quiero tenerlo hoy/mañana)
4. **¿Hay algo que Railway haga mejor/peor que tu recomendación?**
5. **Si algo se rompe, ¿cómo debuggeo?** (acceso a logs/shell)

---

**Documento creado**: 6 Nov 2025  
**Versión**: 1.0  
**Para**: Evaluación de opciones de hosting  
**Proyecto**: LINO Saludable - Sistema de Gestión

---

## 💡 TIP FINAL

Cuando hables con otro asesor, mostrale este documento y pedile:
- "Una recomendación específica de hosting"
- "Pros y contras vs Railway"
- "Pasos específicos para deployar ESTE proyecto"

¡Buena suerte con la investigación! 🚀
