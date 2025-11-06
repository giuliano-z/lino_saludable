# 🚀 GUÍA DE DESPLIEGUE - LINO SALUDABLE

Esta guía te ayudará a desplegar el Sistema LINO en un servidor de producción.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Inicial](#configuración-inicial)
3. [Variables de Entorno](#variables-de-entorno)
4. [Instalación en Servidor](#instalación-en-servidor)
5. [Configuración de Servidor Web](#configuración-de-servidor-web)
6. [Backup Automático](#backup-automático)
7. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
8. [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos Previos

### Servidor
- **Sistema Operativo**: Ubuntu 20.04+ / Debian 11+ (recomendado)
- **RAM**: Mínimo 1GB, recomendado 2GB+
- **Almacenamiento**: Mínimo 10GB libres
- **Python**: 3.11 o superior
- **Usuario sudo**: Acceso con privilegios administrativos

### Dominio y SSL
- Dominio propio (ej: `lino.tuempresa.com`)
- Certificado SSL (recomendado: Let's Encrypt gratis)

---

## ⚙️ Configuración Inicial

### 1. Generar SECRET_KEY nueva

**CRÍTICO**: Nunca usar la SECRET_KEY de desarrollo en producción.

```bash
# Generar SECRET_KEY única
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Guarda este valor de forma segura. Lo necesitarás para las variables de entorno.

### 2. Preparar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# Crear usuario para la aplicación (opcional pero recomendado)
sudo adduser --disabled-password --gecos "" lino
sudo usermod -aG www-data lino
```

---

## 🔐 Variables de Entorno

Crear archivo `.env` en el servidor con las siguientes variables:

```bash
# /home/lino/lino_saludable/.env

# SEGURIDAD (REQUERIDO)
SECRET_KEY='tu-secret-key-generada-aqui'
ALLOWED_HOSTS='lino.tuempresa.com,www.lino.tuempresa.com'

# BASE DE DATOS (Opcional - solo si usas PostgreSQL)
# DB_NAME=lino_saludable
# DB_USER=lino_user
# DB_PASSWORD=tu-password-segura
# DB_HOST=localhost
# DB_PORT=5432

# EMAIL (Opcional - para notificaciones)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_USER=tumail@gmail.com
# EMAIL_PASSWORD=tu-app-password
# ADMIN_EMAIL=admin@tuempresa.com
```

**Seguridad del archivo .env:**
```bash
chmod 600 .env
```

---

## 🖥️ Instalación en Servidor

### Opción A: Despliegue con SQLite (Simple, recomendado para empezar)

```bash
# 1. Clonar repositorio o subir archivos
cd /home/lino
git clone https://github.com/tuusuario/lino_saludable.git
# O usar scp/ftp para subir archivos

# 2. Crear entorno virtual
cd lino_saludable
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Servidor WSGI para producción

# 4. Configurar variables de entorno
# Crear archivo .env según sección anterior

# 5. Cargar variables de entorno
export $(cat .env | xargs)

# 6. Preparar archivos estáticos
cd src
python manage.py collectstatic --noinput --settings=lino_saludable.settings_production

# 7. Aplicar migraciones
python manage.py migrate --settings=lino_saludable.settings_production

# 8. Crear superusuario
python manage.py createsuperuser --settings=lino_saludable.settings_production

# 9. Test del servidor
python manage.py runserver 0.0.0.0:8000 --settings=lino_saludable.settings_production
# Verificar en http://TU_IP:8000
# Presionar Ctrl+C para detener
```

### Opción B: Despliegue con PostgreSQL (Producción seria)

```bash
# 1-3. Igual que Opción A

# 4. Instalar PostgreSQL
sudo apt install -y postgresql postgresql-contrib
pip install psycopg2-binary

# 5. Crear base de datos
sudo -u postgres psql
```

```sql
CREATE DATABASE lino_saludable;
CREATE USER lino_user WITH PASSWORD 'tu-password-segura';
ALTER ROLE lino_user SET client_encoding TO 'utf8';
ALTER ROLE lino_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lino_user SET timezone TO 'America/Argentina/Buenos_Aires';
GRANT ALL PRIVILEGES ON DATABASE lino_saludable TO lino_user;
\q
```

```bash
# 6. Editar settings_production.py y descomentar sección PostgreSQL

# 7-9. Continuar con pasos de Opción A
```

---

## 🌐 Configuración de Servidor Web

### Gunicorn (Servidor de Aplicación)

Crear archivo systemd para auto-inicio:

```bash
sudo nano /etc/systemd/system/lino.service
```

Contenido:

```ini
[Unit]
Description=Gunicorn instance for LINO Saludable
After=network.target

[Service]
User=lino
Group=www-data
WorkingDirectory=/home/lino/lino_saludable/src
Environment="PATH=/home/lino/lino_saludable/venv/bin"
EnvironmentFile=/home/lino/lino_saludable/.env
ExecStart=/home/lino/lino_saludable/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/lino/lino_saludable/lino.sock \
    --timeout 120 \
    --access-logfile /home/lino/lino_saludable/logs/gunicorn_access.log \
    --error-logfile /home/lino/lino_saludable/logs/gunicorn_error.log \
    lino_saludable.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Crear directorio de logs
mkdir -p /home/lino/lino_saludable/logs

# Activar servicio
sudo systemctl start lino
sudo systemctl enable lino
sudo systemctl status lino
```

### Nginx (Reverse Proxy)

```bash
sudo nano /etc/nginx/sites-available/lino
```

Contenido:

```nginx
server {
    listen 80;
    server_name lino.tuempresa.com www.lino.tuempresa.com;

    # Redirigir HTTP → HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lino.tuempresa.com www.lino.tuempresa.com;

    # SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/lino.tuempresa.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lino.tuempresa.com/privkey.pem;
    
    # Seguridad SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    client_max_body_size 10M;

    # Archivos estáticos
    location /static/ {
        alias /home/lino/lino_saludable/src/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/lino/lino_saludable/src/media/;
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://unix:/home/lino/lino_saludable/lino.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    # Logs
    access_log /var/log/nginx/lino_access.log;
    error_log /var/log/nginx/lino_error.log;
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/lino /etc/nginx/sites-enabled/
sudo nginx -t  # Verificar configuración
sudo systemctl restart nginx
```

### Obtener Certificado SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado (interactivo)
sudo certbot --nginx -d lino.tuempresa.com -d www.lino.tuempresa.com

# Auto-renovación (ya viene configurado)
sudo systemctl status certbot.timer
```

---

## 💾 Backup Automático

### Configurar Cron Job

```bash
# Editar crontab
crontab -e
```

Agregar línea:

```cron
# Backup diario a las 2 AM (mantener 7 días)
0 2 * * * cd /home/lino/lino_saludable/src && /home/lino/lino_saludable/venv/bin/python manage.py backup_db --settings=lino_saludable.settings_production >> /home/lino/lino_saludable/logs/backup.log 2>&1
```

### Backup Manual

```bash
# Desde el directorio src/
python manage.py backup_db --settings=lino_saludable.settings_production

# Ver backups
ls -lh ../backups/

# Restaurar backup
cp ../backups/db_backup_20250106_020000.sqlite3 db.sqlite3
python manage.py migrate --settings=lino_saludable.settings_production
```

### Backup Externo (Recomendado)

```bash
# Script para sincronizar a servidor externo
#!/bin/bash
# /home/lino/scripts/sync_backup.sh

BACKUP_DIR="/home/lino/lino_saludable/backups"
REMOTE_SERVER="backup@servidor-backup.com"
REMOTE_PATH="/backups/lino"

# Sincronizar últimos 30 días
rsync -avz --delete \
  --exclude '*.tmp' \
  "$BACKUP_DIR/" \
  "$REMOTE_SERVER:$REMOTE_PATH/"

echo "Backup sincronizado: $(date)" >> /home/lino/lino_saludable/logs/sync.log
```

---

## 📊 Monitoreo y Mantenimiento

### Verificar Estado del Servicio

```bash
# Gunicorn
sudo systemctl status lino

# Nginx
sudo systemctl status nginx

# Ver logs en tiempo real
tail -f /home/lino/lino_saludable/logs/gunicorn_error.log
tail -f /var/log/nginx/lino_error.log
tail -f /home/lino/lino_saludable/src/logs/django_errors.log
```

### Actualizar Aplicación

```bash
cd /home/lino/lino_saludable
source venv/bin/activate

# Hacer backup antes de actualizar
python src/manage.py backup_db --settings=lino_saludable.settings_production

# Actualizar código
git pull origin main
# O subir archivos nuevos via scp

# Instalar nuevas dependencias (si hay)
pip install -r requirements.txt

# Aplicar migraciones
python src/manage.py migrate --settings=lino_saludable.settings_production

# Recolectar estáticos
python src/manage.py collectstatic --noinput --settings=lino_saludable.settings_production

# Reiniciar servicios
sudo systemctl restart lino
sudo systemctl reload nginx
```

### Limpieza de Logs

```bash
# Rotar logs grandes
sudo logrotate /etc/logrotate.d/lino

# Crear configuración de logrotate
sudo nano /etc/logrotate.d/lino
```

```
/home/lino/lino_saludable/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0640 lino www-data
}
```

---

## 🔧 Troubleshooting

### Error 502 Bad Gateway

```bash
# Verificar Gunicorn
sudo systemctl status lino
sudo journalctl -u lino -n 50

# Verificar socket
ls -l /home/lino/lino_saludable/lino.sock

# Permisos
sudo chown lino:www-data /home/lino/lino_saludable/lino.sock
```

### Error 500 Internal Server Error

```bash
# Ver logs de Django
tail -50 /home/lino/lino_saludable/src/logs/django_errors.log

# Ver logs de Gunicorn
tail -50 /home/lino/lino_saludable/logs/gunicorn_error.log

# Verificar SECRET_KEY configurada
echo $SECRET_KEY
```

### Base de Datos Bloqueada (SQLite)

```bash
# Solo si usas SQLite y hay múltiples workers
# Reducir workers en gunicorn.service a 1
# O migrar a PostgreSQL
```

### Archivos Estáticos No se Ven

```bash
# Verificar collectstatic
python manage.py collectstatic --noinput --settings=lino_saludable.settings_production

# Verificar permisos
sudo chown -R lino:www-data /home/lino/lino_saludable/src/staticfiles
sudo chmod -R 755 /home/lino/lino_saludable/src/staticfiles

# Verificar configuración Nginx
sudo nginx -t
```

---

## 📞 Soporte

Si encuentras problemas:

1. Revisar logs (sección Monitoreo)
2. Verificar configuración (variables entorno, permisos)
3. Consultar documentación oficial de Django
4. Contactar al desarrollador

---

## ✅ Checklist de Despliegue

- [ ] SECRET_KEY generada y configurada
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recolectados
- [ ] Gunicorn funcionando y auto-inicio configurado
- [ ] Nginx configurado y SSL activo
- [ ] Backup automático configurado (cron)
- [ ] Logs monitoreados
- [ ] Firewall configurado (puerto 80, 443)
- [ ] Documentación guardada

---

**¡Sistema LINO desplegado y listo para producción!** 🎉
