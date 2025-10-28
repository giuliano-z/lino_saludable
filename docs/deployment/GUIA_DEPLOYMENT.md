# 🚀 GUÍA DE DEPLOYMENT - LINO SALUDABLE EN DIGITALOCEAN

## 📋 RESUMEN EJECUTIVO
Esta guía te permitirá llevar tu sistema LINO SALUDABLE a producción en un servidor DigitalOcean de forma profesional y segura.

## 💰 COSTO ESTIMADO MENSUAL
- **Droplet Básico**: $6/mes (1 vCPU, 1GB RAM, 25GB SSD)
- **Dominio**: $12/año (opcional)
- **Total mensual inicial**: ~$7 USD

---

## 🎯 PASO A PASO - DEPLOYMENT COMPLETO

### **FASE 1: CREAR SERVIDOR EN DIGITALOCEAN**

1. **Crear cuenta en DigitalOcean**
   - Ir a: https://digitalocean.com
   - Crear cuenta (bonus de $200 con referido)

2. **Crear Droplet**
   ```
   - Distribución: Ubuntu 22.04 LTS
   - Plan: Basic - $6/mes (1 vCPU, 1GB RAM, 25GB SSD)
   - Región: New York (mejor latencia para Argentina)
   - Autenticación: SSH Key (más seguro)
   - Hostname: lino-saludable
   ```

3. **Configurar acceso SSH**
   ```bash
   # En tu Mac, generar clave SSH si no tienes:
   ssh-keygen -t ed25519 -C "tu-email@example.com"
   
   # Copiar clave pública al clipboard:
   pbcopy < ~/.ssh/id_ed25519.pub
   
   # Pegar en DigitalOcean al crear el droplet
   ```

### **FASE 2: CONFIGURAR SERVIDOR BASE**

Una vez creado el droplet, conectarse y configurar:

```bash
# 1. Conectar al servidor
ssh root@TU_IP_DEL_DROPLET

# 2. Actualizar sistema
apt update && apt upgrade -y

# 3. Crear usuario para la aplicación
adduser lino
usermod -aG sudo lino
su - lino

# 4. Instalar dependencias básicas
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib curl git

# 5. Configurar firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

### **FASE 3: CONFIGURAR BASE DE DATOS**

```bash
# 1. Configurar PostgreSQL
sudo -u postgres psql

# Dentro de psql:
CREATE DATABASE lino_saludable;
CREATE USER lino_user WITH ENCRYPTED PASSWORD 'TU_PASSWORD_SEGURA';
GRANT ALL PRIVILEGES ON DATABASE lino_saludable TO lino_user;
\q

# 2. Configurar acceso remoto (opcional)
sudo nano /etc/postgresql/14/main/pg_hba.conf
# Añadir línea:
# local   lino_saludable  lino_user   md5
```

### **FASE 4: SUBIR EL CÓDIGO**

```bash
# 1. Clonar repositorio (o subir código)
cd /home/lino
git clone https://github.com/TU_USUARIO/lino_saludable.git
# O usar scp para subir archivos

# 2. Crear entorno virtual
cd lino_saludable
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install psycopg2-binary gunicorn

# 4. Configurar variables de entorno
nano .env
```

### **ARCHIVO .env (CREAR EN EL SERVIDOR)**

```bash
# .env - Variables de producción
DEBUG=False
SECRET_KEY=genera_una_clave_secreta_super_larga_y_compleja_aqui
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,TU_IP_SERVIDOR

# Base de datos
DB_NAME=lino_saludable
DB_USER=lino_user
DB_PASSWORD=TU_PASSWORD_SEGURA
DB_HOST=localhost
DB_PORT=5432

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
ADMIN_EMAIL=admin@tu-dominio.com
```

### **FASE 5: PREPARAR DJANGO PARA PRODUCCIÓN**

```bash
# 1. Ejecutar migraciones
cd src
python manage.py migrate --settings=lino_saludable.settings_production

# 2. Crear superusuario de producción
python manage.py createsuperuser --settings=lino_saludable.settings_production

# 3. Recopilar archivos estáticos
python manage.py collectstatic --settings=lino_saludable.settings_production

# 4. Probar que funciona
python manage.py runserver 0.0.0.0:8000 --settings=lino_saludable.settings_production
# Ctrl+C para parar
```

### **FASE 6: CONFIGURAR GUNICORN**

```bash
# 1. Crear configuración de Gunicorn
nano /home/lino/lino_saludable/gunicorn_config.py
```

**Contenido de gunicorn_config.py:**
```python
bind = "127.0.0.1:8000"
workers = 2
user = "lino"
timeout = 120
keepalive = 5
max_requests = 1000
preload_app = True
```

```bash
# 2. Probar Gunicorn
cd /home/lino/lino_saludable/src
gunicorn --config ../gunicorn_config.py lino_saludable.wsgi:application
```

### **FASE 7: CONFIGURAR NGINX**

```bash
# 1. Crear configuración de Nginx
sudo nano /etc/nginx/sites-available/lino_saludable
```

**Contenido de la configuración:**
```nginx
server {
    listen 80;
    server_name TU_DOMINIO_O_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/lino/lino_saludable/src/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /media/ {
        alias /home/lino/lino_saludable/src/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Logs
    access_log /var/log/nginx/lino_access.log;
    error_log /var/log/nginx/lino_error.log;
}
```

```bash
# 2. Activar sitio
sudo ln -s /etc/nginx/sites-available/lino_saludable /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **FASE 8: CONFIGURAR SERVICIOS SYSTEMD**

```bash
# 1. Crear servicio para Gunicorn
sudo nano /etc/systemd/system/lino_saludable.service
```

**Contenido del servicio:**
```ini
[Unit]
Description=Lino Saludable Django App
After=network.target

[Service]
User=lino
Group=www-data
WorkingDirectory=/home/lino/lino_saludable/src
Environment="DJANGO_SETTINGS_MODULE=lino_saludable.settings_production"
ExecStart=/home/lino/lino_saludable/venv/bin/gunicorn \
          --config /home/lino/lino_saludable/gunicorn_config.py \
          lino_saludable.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 2. Activar y arrancar servicio
sudo systemctl daemon-reload
sudo systemctl enable lino_saludable
sudo systemctl start lino_saludable
sudo systemctl status lino_saludable
```

---

## 🎯 VERIFICACIÓN FINAL

### **Comprobar que todo funciona:**

```bash
# 1. Verificar servicios
sudo systemctl status lino_saludable
sudo systemctl status nginx
sudo systemctl status postgresql

# 2. Verificar logs
sudo tail -f /var/log/nginx/lino_error.log
tail -f /home/lino/lino_saludable/src/logs/business.log

# 3. Probar en navegador
# http://TU_IP_O_DOMINIO
```

---

## 🔒 CONFIGURACIÓN SSL (HTTPS) - OPCIONAL PERO RECOMENDADO

```bash
# 1. Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# 2. Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# 3. Verificar renovación automática
sudo certbot renew --dry-run
```

---

## 📊 MONITOREO Y MANTENIMIENTO

### **Scripts útiles de mantenimiento:**

```bash
# Backup diario de base de datos
pg_dump -U lino_user -h localhost lino_saludable > backup_$(date +%Y%m%d).sql

# Ver logs en tiempo real
tail -f /home/lino/lino_saludable/src/logs/*.log

# Reiniciar aplicación
sudo systemctl restart lino_saludable

# Actualizar código
cd /home/lino/lino_saludable
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python src/manage.py migrate --settings=lino_saludable.settings_production
python src/manage.py collectstatic --settings=lino_saludable.settings_production --noinput
sudo systemctl restart lino_saludable
```

---

## 🆘 TROUBLESHOOTING

### **Problemas comunes:**

1. **Error 502 Bad Gateway**: Verificar que Gunicorn esté ejecutándose
2. **Error de permisos**: `sudo chown -R lino:www-data /home/lino/lino_saludable`
3. **Base de datos no conecta**: Verificar configuración en .env
4. **Archivos estáticos no cargan**: Ejecutar collectstatic nuevamente

---

## 🎉 ¡ÉXITO!

Si seguiste todos los pasos, tu sistema LINO SALUDABLE estará funcionando en producción con:

✅ **Base de datos PostgreSQL**  
✅ **Servidor web Nginx**  
✅ **Aplicación Django con Gunicorn**  
✅ **Logs detallados**  
✅ **Backups automáticos**  
✅ **SSL/HTTPS (opcional)**  
✅ **Monitoreo básico**  

**¡Tu sistema está listo para generar dinero real!** 💰
