"""
Configuración para entorno de producción
Separamos la configuración para mayor seguridad y control
"""
import os
from .settings import *

# ==================== CONFIGURACIÓN DE PRODUCCIÓN ====================

# SECURITY WARNING: En producción usar variables de entorno
DEBUG = False

# Hosts permitidos - CAMBIAR por tu dominio real
ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    '127.0.0.1',
    'localhost',
]

# ==================== BASE DE DATOS DE PRODUCCIÓN ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'lino_saludable'),
        'USER': os.getenv('DB_USER', 'lino_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'change_this_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}

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

# ==================== SEGURIDAD ====================
# En producción, usar HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Sessions más seguras
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# ==================== ARCHIVOS ESTÁTICOS ====================
STATIC_ROOT = '/var/www/lino_saludable/static/'

# ==================== CACHÉ (para mejorar performance) ====================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
        'TIMEOUT': 300,  # 5 minutos
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# ==================== EMAIL (para notificaciones) ====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# Email para notificaciones críticas
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@tu-dominio.com')
