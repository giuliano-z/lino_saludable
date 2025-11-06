#!/bin/bash
# Script para hacer commit y push de la limpieza

echo "🧹 LIMPIEZA DE PROYECTO LINO SALUDABLE"
echo "========================================"
echo ""
echo "📝 Resumen de cambios:"
echo "   - 23 archivos eliminados (conflictivos y temporales)"
echo "   - 4 archivos nuevos (railway.toml, .slugignore, docs)"
echo "   - 2 archivos mejorados (nixpacks.toml, createusers.py)"
echo ""
echo "¿Deseas continuar con el commit? (y/n)"
read -r response

if [[ "$response" != "y" ]]; then
    echo "❌ Operación cancelada"
    exit 0
fi

echo ""
echo "📦 Agregando cambios a Git..."
git add .

echo ""
echo "💾 Creando commit..."
git commit -m "🧹 Limpieza proyecto Railway

✨ Cambios principales:
- Eliminados archivos conflictivos (Procfile, server.js, package.json)
- Eliminados scripts temporales (run_migrations_railway.py, migrate.sh, start.sh)
- Eliminados archivos de testing (test_*.py, check_*.py, etc.)
- Creado railway.toml como configuración principal
- Creado .slugignore para optimizar build
- Mejorado createusers.py con soporte para variables de entorno
- Simplificado nixpacks.toml

🎯 Objetivo: Despliegue limpio en Railway con ejecución automática de migraciones

Archivos eliminados: 23
Archivos nuevos: 4
Archivos mejorados: 2"

echo ""
echo "🚀 ¿Deseas hacer push a origin main? (y/n)"
read -r push_response

if [[ "$push_response" == "y" ]]; then
    echo ""
    echo "⬆️  Haciendo push..."
    git push origin main
    echo ""
    echo "✅ CAMBIOS SUBIDOS EXITOSAMENTE"
    echo ""
    echo "📊 Próximos pasos:"
    echo "   1. Ve a Railway: https://railway.app/project/<tu-proyecto>"
    echo "   2. Verifica que el deploy inicie automáticamente"
    echo "   3. Monitorea los logs para ver:"
    echo "      - Running migrations..."
    echo "      - Creating users..."
    echo "      - Starting gunicorn..."
    echo "   4. Accede a: https://web-production-b0ad1.up.railway.app/admin/"
    echo "   5. ¡Cambia las contraseñas inmediatamente!"
    echo ""
else
    echo ""
    echo "✅ Commit creado localmente"
    echo "⚠️  Recuerda hacer push cuando estés listo:"
    echo "   git push origin main"
    echo ""
fi

echo "🎉 ¡Listo!"
