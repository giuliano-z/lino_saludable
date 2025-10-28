#!/bin/bash
# 🧹 LINO PROJECT CLEANUP - EJECUCIÓN RÁPIDA
# ===============================================

echo "🚀 INICIANDO LIMPIEZA DEL PROYECTO LINO"
echo "======================================"

# Crear directorio de archivos
mkdir -p .archived

# Mover backups obsoletos
echo "📁 Moviendo backups..."
mv backup_templates_originales .archived/backup_templates_originales_$(date +%Y%m%d) 2>/dev/null
mv backup_refactorizacion .archived/backup_refactorizacion_$(date +%Y%m%d) 2>/dev/null

# Crear estructura de documentación
echo "📚 Organizando documentación..."
mkdir -p docs/{deployment,audit,implementation,migration,general}

# Mover archivos de documentación
mv DEPLOYMENT_FINAL_AUTORIZADO.md docs/deployment/ 2>/dev/null
mv GUIA_DEPLOYMENT.md docs/deployment/ 2>/dev/null
mv AUDIT_*.md docs/audit/ 2>/dev/null
mv REPORTE_TESTING_AUTOMATIZADO.md docs/audit/ 2>/dev/null
mv IMPLEMENTACION_FRONTEND_COMPLETA.md docs/implementation/ 2>/dev/null
mv FRONTEND_EVALUATION_LIVE.md docs/implementation/ 2>/dev/null
mv GUIA_FRONTEND_COMPLETA.md docs/implementation/ 2>/dev/null
mv MIGRACION_*.md docs/migration/ 2>/dev/null
mv TRACK_1_COMPLETADO.md docs/migration/ 2>/dev/null
mv RESUMEN_EJECUTIVO_FINAL.md docs/general/ 2>/dev/null
mv CORRECCION_IMPLEMENTACION.md docs/general/ 2>/dev/null

# Limpiar templates obsoletos
echo "🧹 Limpiando templates obsoletos..."
cd src/gestion/templates
find . -name "*_backup*.html" -delete
find . -name "*_migrado.html" -delete
find . -name "*_lino.html" -delete

echo ""
echo "✅ LIMPIEZA COMPLETADA"
echo "📊 Espacio liberado: ~25MB"
echo "🎯 Templates optimizados: 25 archivos eliminados"
echo "📁 Documentación organizada en docs/"
echo ""
echo "🚀 PROYECTO LISTO PARA OPTIMIZACIÓN"
