# 🔒 PLAN: BACKUPS AUTOMÁTICOS PARA LINO SALUDABLE

**Fecha:** 9 de Diciembre 2025  
**Prioridad:** 🔴 ALTA  
**Estado:** 📋 PLANIFICADO

---

## 🎯 OBJETIVO

Implementar sistema de backups automáticos diarios para:
- ✅ Proteger datos del cliente
- ✅ Recuperación rápida ante fallos
- ✅ Auditoría histórica
- ✅ Cumplimiento de mejores prácticas

---

## 📊 ANÁLISIS DE OPCIONES

### **OPCIÓN 1: Backups Nativos de Railway** ⭐ RECOMENDADO

**Características:**
- ✅ Integrado en Railway
- ✅ Backups automáticos diarios
- ✅ Point-in-time recovery
- ✅ Sin código adicional
- ✅ Restauración con 1 click

**Costo:**
- Railway Pro Plan: $5-20/mes (incluye backups)
- O Pro Plan de PostgreSQL: ~$5/mes adicional

**Implementación:**
```
1. Railway Dashboard
2. PostgreSQL → Settings
3. Enable "Automated Backups"
4. Configurar:
   - Frecuencia: Diaria
   - Hora: 3:00 AM
   - Retención: 7-30 días
   - Notificaciones: Email
```

**Pros:**
- ✅ Configuración en 5 minutos
- ✅ Mantenimiento cero
- ✅ Confiable (Railway lo gestiona)
- ✅ Restauración simple

**Contras:**
- 💰 Costo mensual adicional
- ⚠️ Dependencia de Railway

---

### **OPCIÓN 2: Script Python + Cron Job**

**Características:**
- ✅ Gratis (sin costos adicionales)
- ✅ Control total
- ✅ Backup a múltiples destinos
- ✅ Personalizable

**Implementación:**

#### Paso 1: Script de Backup
```python
# scripts/backup_automatico.py

import os
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup automático de base de datos'
    
    def handle(self, *args, **kwargs):
        # 1. Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_lino_{timestamp}.sql'
        backup_path = f'/backups/{backup_file}'
        
        # 2. Variables de conexión desde settings
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        
        # 3. Ejecutar pg_dump
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = db_password
            
            cmd = [
                'pg_dump',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-F', 'c',  # Custom format (comprimido)
                '-b',       # Include large objects
                '-v',       # Verbose
                '-f', backup_path,
                db_name
            ]
            
            subprocess.run(cmd, env=env, check=True)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Backup creado: {backup_file}')
            )
            
            # 4. Subir a storage externo (opcional)
            self.upload_to_cloud(backup_path)
            
            # 5. Limpiar backups antiguos (> 30 días)
            self.cleanup_old_backups()
            
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error en backup: {e}')
            )
            raise
    
    def upload_to_cloud(self, backup_path):
        """Subir backup a AWS S3, Google Drive, etc."""
        # Implementar según servicio elegido
        pass
    
    def cleanup_old_backups(self):
        """Eliminar backups > 30 días"""
        # Implementar lógica de limpieza
        pass
```

#### Paso 2: GitHub Actions Workflow
```yaml
# .github/workflows/backup.yml

name: Backup Automático Diario

on:
  schedule:
    - cron: '0 3 * * *'  # 3 AM todos los días
  workflow_dispatch:      # Manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run backup
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          python src/manage.py backup_automatico
      
      - name: Upload to S3
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
        
      - name: Sync to S3
        run: |
          aws s3 sync backups/ s3://lino-saludable-backups/ \
            --exclude "*" \
            --include "backup_lino_*.sql"
      
      - name: Notify success
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: '✅ Backup diario completado'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

**Pros:**
- ✅ Gratis (excepto storage externo)
- ✅ Control total del proceso
- ✅ Múltiples destinos de backup

**Contras:**
- ⚠️ Requiere implementación
- ⚠️ Mantenimiento manual
- ⚠️ Necesita storage externo (S3, Drive)

---

### **OPCIÓN 3: Servicio de Backup Externo**

**Opciones:**
- **SimpleBackups.com** - $15/mes, automatizado
- **BackupNinja** - $10/mes
- **Rewind Backups** - $5-20/mes

**Pros:**
- ✅ Configuración simple
- ✅ Gestión profesional
- ✅ Múltiples destinos
- ✅ Monitoreo incluido

**Contras:**
- 💰 Costo mensual
- ⚠️ Dependencia de tercero

---

## 🎯 RECOMENDACIÓN: PLAN HÍBRIDO

### **Fase 1: Inmediato (Esta Semana)**
✅ **Activar Railway Automated Backups**
- Costo: ~$5/mes adicional
- Tiempo: 5 minutos
- Protección básica inmediata

### **Fase 2: Corto Plazo (Próximo Sprint)**
✅ **Implementar Script de Backup Python**
- Backup manual on-demand
- Comando: `python manage.py backup_automatico`
- Guardar en carpeta local + upload a Google Drive

### **Fase 3: Mediano Plazo (Próximo Mes)**
✅ **GitHub Actions Workflow**
- Backup automático diario vía CI/CD
- Upload a AWS S3 (costo ~$1/mes por storage)
- Notificaciones por email

---

## 📋 IMPLEMENTACIÓN PASO A PASO

### **PASO 1: Railway Backups (HOY)**

```bash
# 1. Ir a Railway Dashboard
# 2. Proyecto lino_saludable → PostgreSQL
# 3. Settings → Backups
# 4. Enable "Automated Backups"
# 5. Configurar:
#    - Frequency: Daily
#    - Time: 03:00 (3 AM)
#    - Retention: 7 days (Pro) o 30 days (Team)
# 6. Save
```

**Costo estimado:** $5-10/mes adicional

---

### **PASO 2: Script de Backup Manual (Esta Semana)**

```bash
# 1. Crear archivo
touch src/gestion/management/commands/backup_database.py

# 2. Implementar comando Django (código arriba)

# 3. Test local
python src/manage.py backup_database

# 4. Verificar que crea archivo .sql

# 5. Commit y push
git add src/gestion/management/commands/backup_database.py
git commit -m "feat: agregar comando de backup manual"
git push
```

**Uso:**
```bash
# Desde Railway CLI o shell
railway run python src/manage.py backup_database
```

---

### **PASO 3: Almacenamiento Externo (Próxima Semana)**

**Opción A: Google Drive API**
```bash
pip install google-api-python-client google-auth

# Configurar credenciales OAuth2
# Upload automático a carpeta Drive
```

**Opción B: AWS S3**
```bash
pip install boto3

# Configurar AWS credentials
# Upload a bucket S3
# Costo: ~$0.023/GB/mes
```

**Opción C: Dropbox**
```bash
pip install dropbox

# Más simple que S3
# Plan gratis: 2GB
```

---

### **PASO 4: Automatización con GitHub Actions**

```bash
# 1. Crear archivo workflow
mkdir -p .github/workflows
touch .github/workflows/daily-backup.yml

# 2. Agregar código YAML (ver arriba)

# 3. Configurar secrets en GitHub:
#    - DATABASE_URL
#    - AWS_ACCESS_KEY_ID (si usas S3)
#    - AWS_SECRET_ACCESS_KEY

# 4. Commit y push
git add .github/workflows/daily-backup.yml
git commit -m "ci: agregar backup automático diario"
git push

# 5. Verificar en GitHub Actions tab
```

---

## 📊 COMPARACIÓN DE COSTOS

| Solución | Costo Mensual | Setup Time | Mantenimiento |
|----------|---------------|------------|---------------|
| Railway Native | $5-10 | 5 min | ✅ Cero |
| Script Python + Local | $0 | 2 horas | ⚠️ Manual |
| GitHub Actions + S3 | ~$1-3 | 3 horas | ✅ Bajo |
| SimpleBackups | $15 | 10 min | ✅ Cero |
| **Plan Híbrido** | **$5-10** | **1 hora** | **✅ Bajo** |

---

## 🎯 ROADMAP DE IMPLEMENTACIÓN

### **Semana 1 (Esta Semana):**
- [x] Deploy de fix de bugs ← AHORA
- [ ] Activar Railway Automated Backups
- [ ] Crear script de backup manual
- [ ] Test de backup manual

### **Semana 2:**
- [ ] Implementar upload a Google Drive
- [ ] Documentar proceso de restauración
- [ ] Test de restauración completa

### **Semana 3:**
- [ ] GitHub Actions workflow
- [ ] Notificaciones automáticas
- [ ] Dashboard de backups

### **Semana 4:**
- [ ] Monitoreo de tamaño de backups
- [ ] Optimización de storage
- [ ] Documentación para cliente

---

## 📚 DOCUMENTACIÓN A CREAR

1. **MANUAL_BACKUPS.md**
   - Cómo hacer backup manual
   - Cómo restaurar backup
   - Troubleshooting

2. **DISASTER_RECOVERY_PLAN.md**
   - Plan completo de recuperación
   - SLA de recuperación (< 1 hora)
   - Contactos de emergencia

3. **BACKUP_MONITORING.md**
   - Cómo verificar que backups funcionan
   - Métricas a monitorear
   - Alertas configuradas

---

## ✅ CHECKLIST DE BACKUPS

### Setup Inicial:
- [ ] Railway Automated Backups activado
- [ ] Script de backup manual implementado
- [ ] Test de backup exitoso
- [ ] Test de restauración exitoso
- [ ] Documentación creada

### Operación Diaria:
- [ ] Backup automático ejecutado
- [ ] Archivo generado correctamente
- [ ] Upload a storage externo OK
- [ ] Tamaño de archivo razonable
- [ ] Notificación recibida

### Mantenimiento Mensual:
- [ ] Verificar integridad de backups
- [ ] Test de restauración completa
- [ ] Limpiar backups antiguos (> 30 días)
- [ ] Revisar costos de storage
- [ ] Actualizar documentación

---

## 🚨 PLAN DE RECUPERACIÓN

### Escenario 1: Pérdida de Datos (< 24 horas)
```bash
# 1. Identificar último backup válido
# 2. Descargar desde Railway/S3
# 3. Restaurar en Railway:
railway pg:restore backup_lino_YYYYMMDD.sql

# 4. Verificar datos
# 5. Notificar cliente
```

**Tiempo estimado:** 15-30 minutos

---

### Escenario 2: Corrupción de Base de Datos
```bash
# 1. Detener aplicación
railway down

# 2. Crear nueva database
railway pg:create lino_saludable_restored

# 3. Restaurar backup
railway pg:restore -d lino_saludable_restored backup.sql

# 4. Actualizar DATABASE_URL
railway variables:set DATABASE_URL=...

# 5. Reiniciar app
railway up
```

**Tiempo estimado:** 30-60 minutos

---

### Escenario 3: Disaster Recovery Completo
```bash
# Si Railway falla completamente:

# 1. Nuevo proyecto Railway
# 2. Nueva database PostgreSQL
# 3. Restaurar último backup
# 4. Deploy código desde GitHub
# 5. Configurar variables de entorno
# 6. DNS a nueva URL
# 7. Verificar todo funciona
```

**Tiempo estimado:** 2-4 horas

---

## 💰 PRESUPUESTO ESTIMADO

### Opción Económica ($5-10/mes):
- Railway Automated Backups: $5/mes
- **Total: $5/mes**

### Opción Profesional ($10-20/mes):
- Railway Pro Plan: $10/mes
- AWS S3 Storage: $1-3/mes
- GitHub Actions: Gratis
- **Total: $11-13/mes**

### Opción Enterprise ($50+/mes):
- Railway Team Plan: $20/mes
- Dedicated Backup Service: $15/mes
- Monitoring (Sentry): $26/mes
- **Total: $61/mes**

---

## 🎯 RECOMENDACIÓN FINAL

### **Para LINO Saludable (Proyecto Pequeño):**

✅ **Plan Recomendado: Híbrido Económico**

1. **Railway Automated Backups** ($5/mes)
   - Setup: Esta semana
   - Backup diario automático
   - Retención: 7 días

2. **Script Manual de Backup** (Gratis)
   - Para backups on-demand
   - Antes de cambios importantes

3. **GitHub Actions + Google Drive** (Gratis)
   - Backup semanal a Drive
   - Retención: 30 días
   - Storage: 15GB gratis de Google

**Costo Total: $5/mes**  
**Protección: Excelente**  
**Setup: 1-2 horas**

---

## 📝 PRÓXIMOS PASOS

Después del deploy de hoy:

1. **Hoy:** Activar Railway Automated Backups
2. **Mañana:** Crear script de backup manual
3. **Esta Semana:** Test completo de restauración
4. **Próxima Semana:** GitHub Actions workflow

---

**¿Procedemos con este plan?** 🚀

Después del deploy exitoso, podemos empezar con Railway Backups inmediatamente.
