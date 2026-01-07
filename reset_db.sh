#!/bin/bash
# Script para resetear la base de datos de Railway
# Se ejecuta manualmente después del deploy

echo "========================================"
echo "🔄 RESETEANDO BASE DE DATOS"
echo "========================================"

cd src
python manage.py reset_production --confirm << EOF
RESETEAR PRODUCCION
EOF

echo "✅ Reset completado"
