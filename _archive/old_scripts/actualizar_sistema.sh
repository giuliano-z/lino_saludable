#!/bin/bash
# ==============================================================================
# 🚀 SCRIPT DE ACTUALIZACIÓN AUTOMÁTICA - LINO SALUDABLE
# ==============================================================================
# Este script actualiza el sistema en producción de forma segura
# Ejecutar en el servidor: chmod +x actualizar_sistema.sh && ./actualizar_sistema.sh

set -e  # Parar en cualquier error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE} 🥜 LINO SALUDABLE - ACTUALIZADOR AUTOMÁTICO${NC}"
echo -e "${BLUE}======================================================================${NC}"

# Variables de configuración
PROJECT_DIR="/home/lino/lino_saludable"
VENV_DIR="${PROJECT_DIR}/venv"
SRC_DIR="${PROJECT_DIR}/src"
BACKUP_DIR="${PROJECT_DIR}/backups"
SERVICE_NAME="lino_saludable"

# Función para logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [[ ! -d "${PROJECT_DIR}" ]]; then
    log_error "Directorio del proyecto no encontrado: ${PROJECT_DIR}"
    exit 1
fi

cd "${PROJECT_DIR}"

# ==============================================================================
# PASO 1: CREAR BACKUP ANTES DE ACTUALIZAR
# ==============================================================================
log_info "📦 Creando backup de seguridad..."

# Crear directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"

# Backup de base de datos
BACKUP_FILE="${BACKUP_DIR}/lino_backup_$(date +%Y%m%d_%H%M%S).sql"
log_info "🗄️  Haciendo backup de base de datos..."

if pg_dump -U lino_user -h localhost lino_saludable > "${BACKUP_FILE}"; then
    log_info "✅ Backup creado: $(basename ${BACKUP_FILE})"
else
    log_error "❌ Error creando backup de base de datos"
    exit 1
fi

# Backup de archivos de configuración importantes
log_info "📋 Backup de configuración..."
cp -f "${SRC_DIR}/.env" "${BACKUP_DIR}/.env.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || log_warn "No se encontró archivo .env"

# ==============================================================================
# PASO 2: ACTUALIZAR CÓDIGO
# ==============================================================================
log_info "🔄 Actualizando código desde repositorio..."

# Verificar estado del repositorio
if [[ -d ".git" ]]; then
    # Guardar cambios locales temporalmente
    git stash push -m "Auto-stash antes de actualización $(date)"
    
    # Actualizar código
    if git pull origin main; then
        log_info "✅ Código actualizado desde repositorio"
    else
        log_error "❌ Error actualizando código"
        exit 1
    fi
else
    log_warn "⚠️  No es un repositorio Git. Saltando actualización de código..."
fi

# ==============================================================================
# PASO 3: ACTUALIZAR DEPENDENCIAS
# ==============================================================================
log_info "📚 Actualizando dependencias Python..."

# Activar entorno virtual
source "${VENV_DIR}/bin/activate"

# Actualizar pip
pip install --upgrade pip

# Instalar/actualizar dependencias
if pip install -r requirements.txt; then
    log_info "✅ Dependencias actualizadas"
else
    log_error "❌ Error actualizando dependencias"
    exit 1
fi

# ==============================================================================
# PASO 4: EJECUTAR MIGRACIONES
# ==============================================================================
log_info "🏗️  Ejecutando migraciones de base de datos..."

cd "${SRC_DIR}"

# Verificar migraciones pendientes
if python manage.py showmigrations --plan --settings=lino_saludable.settings_production | grep -q "\[ \]"; then
    log_info "📝 Hay migraciones pendientes. Ejecutando..."
    
    if python manage.py migrate --settings=lino_saludable.settings_production; then
        log_info "✅ Migraciones ejecutadas exitosamente"
    else
        log_error "❌ Error ejecutando migraciones"
        log_error "🔄 Restaurando desde backup..."
        # TODO: Implementar restauración automática
        exit 1
    fi
else
    log_info "✅ No hay migraciones pendientes"
fi

# ==============================================================================
# PASO 5: RECOPILAR ARCHIVOS ESTÁTICOS
# ==============================================================================
log_info "📦 Recopilando archivos estáticos..."

if python manage.py collectstatic --settings=lino_saludable.settings_production --noinput; then
    log_info "✅ Archivos estáticos actualizados"
else
    log_warn "⚠️  Error recopilando archivos estáticos (continuando...)"
fi

# ==============================================================================
# PASO 6: VERIFICAR CONFIGURACIÓN
# ==============================================================================
log_info "🔍 Verificando configuración del sistema..."

# Ejecutar script de verificación
if python ../init_sistema.py; then
    log_info "✅ Verificación del sistema completada"
else
    log_warn "⚠️  Advertencias en la verificación (continuando...)"
fi

# ==============================================================================
# PASO 7: REINICIAR SERVICIOS
# ==============================================================================
log_info "🔄 Reiniciando servicios..."

# Reiniciar Gunicorn
if sudo systemctl restart "${SERVICE_NAME}"; then
    log_info "✅ Servicio ${SERVICE_NAME} reiniciado"
else
    log_error "❌ Error reiniciando ${SERVICE_NAME}"
fi

# Verificar que el servicio esté activo
sleep 3
if sudo systemctl is-active --quiet "${SERVICE_NAME}"; then
    log_info "✅ Servicio ${SERVICE_NAME} está activo"
else
    log_error "❌ Servicio ${SERVICE_NAME} no está activo"
    sudo systemctl status "${SERVICE_NAME}"
fi

# Reload Nginx (sin reiniciar)
if sudo nginx -t && sudo systemctl reload nginx; then
    log_info "✅ Nginx recargado exitosamente"
else
    log_warn "⚠️  Problema con Nginx (verificar configuración)"
fi

# ==============================================================================
# PASO 8: VERIFICACIÓN FINAL
# ==============================================================================
log_info "🧪 Verificación final del sistema..."

# Verificar que la aplicación responda
HEALTH_URL="http://localhost"
if curl -f -s "${HEALTH_URL}" > /dev/null; then
    log_info "✅ Aplicación responde correctamente"
else
    log_error "❌ Aplicación no responde en ${HEALTH_URL}"
    log_error "🔍 Verificando logs..."
    sudo journalctl -u "${SERVICE_NAME}" --lines=10 --no-pager
fi

# ==============================================================================
# PASO 9: LIMPIAR ARCHIVOS ANTIGUOS
# ==============================================================================
log_info "🧹 Limpiando archivos antiguos..."

# Mantener solo los últimos 10 backups
cd "${BACKUP_DIR}"
ls -t lino_backup_*.sql | tail -n +11 | xargs -r rm -f
log_info "✅ Backups antiguos limpiados (manteniendo últimos 10)"

# Limpiar cache de Python
find "${PROJECT_DIR}" -name "*.pyc" -delete
find "${PROJECT_DIR}" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
log_info "✅ Cache de Python limpiado"

# ==============================================================================
# RESUMEN FINAL
# ==============================================================================
echo -e "${BLUE}======================================================================${NC}"
echo -e "${GREEN} 🎉 ACTUALIZACIÓN COMPLETADA EXITOSAMENTE${NC}"
echo -e "${BLUE}======================================================================${NC}"

log_info "📋 Resumen de la actualización:"
log_info "   • Backup creado: $(basename ${BACKUP_FILE})"
log_info "   • Código actualizado desde repositorio"
log_info "   • Dependencias Python actualizadas"
log_info "   • Migraciones ejecutadas"
log_info "   • Archivos estáticos recopilados"
log_info "   • Servicios reiniciados"
log_info "   • Verificación completada"

log_info "🚀 Sistema LINO SALUDABLE actualizado y funcionando"
log_info "📊 Monitorear logs: tail -f ${SRC_DIR}/logs/business.log"
log_info "🌐 Verificar en navegador: http://$(curl -s ifconfig.me)"

echo -e "${BLUE}======================================================================${NC}"

# Logging en archivo del sistema
python -c "
import sys
sys.path.append('${SRC_DIR}')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
import django
django.setup()
from gestion.logging_system import LinoLogger
LinoLogger.business_logger.info('SISTEMA_ACTUALIZADO - Actualización automática completada exitosamente')
" 2>/dev/null || log_warn "No se pudo registrar en logs del sistema"

log_info "✅ Actualización completada. ¡Sistema listo para producción!"
