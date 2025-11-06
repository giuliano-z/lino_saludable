"""
Configuración para entorno de producción
Separamos la configuración para mayor seguridad y control

IMPORTANTE: Configurar las siguientes variables de entorno:
- SECRET_KEY: Clave secreta única (generar nueva, no usar la de desarrollo)
- ALLOWED_HOSTS: Dominio del servidor (ej: lino.miempresa.com)
- DB_NAME, DB_USER, DB_PASSWORD: Credenciales de PostgreSQL (opcional)
"""
import os
from .settings import *

# ==================== CONFIGURACIÓN DE PRODUCCIÓN ====================

# SECRET_KEY desde variable de entorno (CRÍTICO)
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
if SECRET_KEY == 'django-insecure-wexdri($&@tjf@x(6&xmv0pi=b-5ye49$%&a5d0b39-ty3h@vw':
    import warnings
    warnings.warn('⚠️  ADVERTENCIA: Usando SECRET_KEY de desarrollo. Configurar SECRET_KEY en variables de entorno.')

# DEBUG DEBE SER FALSE en producción
DEBUG = False

# Hosts permitidos - Desde variable de entorno o configuración manual
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'tu-dominio.com,www.tu-dominio.com')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',')]
ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])  # Siempre permitir local

# ==================== BASE DE DATOS DE PRODUCCIÓN ====================
# Opción 1: SQLite (Simple, para empezar)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Opción 2: PostgreSQL (Recomendado para producción seria)
# Descomentar si se usa PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME', 'lino_saludable'),
#         'USER': os.getenv('DB_USER', 'lino_user'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),  # REQUERIDO desde variable entorno
#         'HOST': os.getenv('DB_HOST', 'localhost'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#         'CONN_MAX_AGE': 600,  # Conexiones persistentes
#     }
# }

# ==================== CONFIGURACIÓN DE LOGGING PROFESIONAL ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'business': {
            'format': '[LINO] {asctime} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Archivo general de errores
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        # Archivo para operaciones de negocio críticas
        'business_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'business.log'),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'business',
        },
        # Archivo para ventas (crítico)
        'ventas_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'ventas.log'),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10,  # Más backups para ventas
            'formatter': 'business',
        },
        # Archivo para stock (crítico)
        'stock_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'stock.log'),
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 10,  # Más backups para stock
            'formatter': 'business',
        },
        # Console para desarrollo
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        # Logger general de Django
        'django': {
            'handlers': ['error_file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        # Logger específico para operaciones de negocio
        'lino.business': {
            'handlers': ['business_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Logger específico para ventas
        'lino.ventas': {
            'handlers': ['ventas_file', 'business_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Logger específico para stock
        'lino.stock': {
            'handlers': ['stock_file', 'business_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Logger para toda la app gestion
        'gestion': {
            'handlers': ['business_file', 'error_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ==================== SEGURIDAD AVANZADA ====================
# HTTPS/SSL (Requerido para producción web)
SECURE_SSL_REDIRECT = True  # Redirigir HTTP → HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True  # Filtro XSS del navegador
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevenir MIME sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevenir clickjacking

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Sessions más seguras (cookies solo HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'

# ==================== ARCHIVOS ESTÁTICOS ====================
STATIC_ROOT = '/var/www/lino_saludable/static/'

# ==================== CACHÉ (para Rate Limiting y Performance) ====================
# PRODUCCIÓN: Usar Redis para rate limiting y cache
# Instalar: sudo apt install redis-server && pip install redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'TIMEOUT': 300,  # 5 minutos
        'OPTIONS': {
            'MAX_CONNECTIONS': 50,
        }
    }
}

# Alternativa si no tienes Redis: usar locmem (solo 1 worker de Gunicorn)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'ratelimit-cache',
#     }
# }

# ==================== 🛡️ RATE LIMITING ====================
RATELIMIT_ENABLE = True  # ACTIVADO en producción
RATELIMIT_USE_CACHE = 'default'

# Límites de tasa (ajustar según necesidad)
RATELIMIT_LOGIN = '5/m'  # 5 intentos de login por minuto
RATELIMIT_VENTAS = '30/h'  # 30 ventas por hora
RATELIMIT_COMPRAS = '20/h'  # 20 compras por hora
RATELIMIT_PRODUCTOS = '50/h'  # 50 productos creados/editados por hora

# ==================== EMAIL (para notificaciones) ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# Email para notificaciones críticas
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@tu-dominio.com')
