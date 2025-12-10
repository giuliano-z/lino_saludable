# 🧹 AUDITORÍA DE LIMPIEZA - DICIEMBRE 2025

**Fecha:** 2 de Diciembre 2025
**Objetivo:** Limpiar archivos obsoletos, duplicados y que estorban
**Principio:** Simplicidad - mantener solo lo esencial

---

## 📊 ANÁLISIS DE ARCHIVOS A ELIMINAR

### ❌ CARPETAS COMPLETAS A ELIMINAR

#### 1. `_cleanup_backup_20251020/` (4.5 MB aprox)
**Motivo:** Backup antiguo de limpieza de octubre
**Contenido:** 
- Templates antiguos
- CSS duplicados
- JS obsoletos
**Acción:** ELIMINAR COMPLETO

#### 2. `_archive/` 
**Motivo:** Archivos archivados que no se usan
**Contenido:**
- old_scripts
- old_docs  
- old_reports
**Acción:** ELIMINAR COMPLETO

#### 3. `.archived/`
**Motivo:** Backups de refactorización de octubre
**Contenido:**
- backup_templates_originales_20251001
- backup_refactorizacion_20251001
**Acción:** ELIMINAR COMPLETO

---

### ⚠️ ARCHIVOS ESPECÍFICOS A ELIMINAR

#### En `src/gestion/templates/`

```
❌ gestion/_backup_templates/          # Templates de backup
❌ gestion/_old/                       # Templates antiguos
❌ _obsolete_templates/                # Templates obsoletos
❌ modules/productos/lista_productos_CORRUPTED.html
❌ dashboard_rentabilidad_old.html
```

#### Scripts temporales en raíz

```
❌ audit_production.py
❌ investigate_stock_bug.py
❌ test_e2e_manual.py
❌ verify_dashboard_manual.py
❌ verify_dashboard_simple.py
❌ commit_limpieza.sh
❌ migrate.sh
```

---

## ✅ ARCHIVOS QUE MANTENER

### Documentación importante
```
✅ README.md
✅ CHECKLIST.md
✅ MANUAL_USUARIO_COMPLETO.md
✅ MANUAL_RESUMIDO.md
✅ MANUAL_PARTE_*.md (2-6)
✅ docs/PRODUCTION_READY_FINAL.md
✅ docs/BUGS_CORREGIDOS_COMPLETO.md
```

### Configuración esencial
```
✅ requirements.txt
✅ runtime.txt
✅ railway.toml
✅ nixpacks.toml
✅ Procfile
✅ pytest.ini
✅ conftest.py
```

### Tests
```
✅ tests_e2e/ (si contiene tests válidos)
✅ src/gestion/tests/
✅ src/gestion/tests_gestion/
```

---

## 📋 PLAN DE LIMPIEZA

### Fase 1: Eliminar carpetas grandes (SEGURO)
```bash
rm -rf _cleanup_backup_20251020
rm -rf _archive
rm -rf .archived
```

### Fase 2: Limpiar templates obsoletos
```bash
rm -rf src/gestion/templates/gestion/_backup_templates
rm -rf src/gestion/templates/gestion/_old
rm -rf src/gestion/templates/_obsolete_templates
rm src/gestion/templates/modules/productos/lista_productos_CORRUPTED.html
rm src/gestion/templates/gestion/dashboard_rentabilidad_old.html
```

### Fase 3: Limpiar scripts temporales en raíz
```bash
rm audit_production.py
rm investigate_stock_bug.py
rm test_e2e_manual.py
rm verify_dashboard_manual.py
rm verify_dashboard_simple.py
rm commit_limpieza.sh
rm migrate.sh
```

### Fase 4: Limpiar documentos duplicados en docs/
```bash
cd docs/
# Revisar manualmente y eliminar duplicados
```

---

## 🎯 ESTRUCTURA FINAL PROPUESTA

```
lino_saludable/
├── src/                      # Código fuente
│   ├── lino_saludable/      # Settings
│   ├── gestion/             # App principal
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── services/
│   │   ├── templates/gestion/  # Solo templates actuales
│   │   ├── static/gestion/
│   │   ├── tests/
│   │   └── management/
│   ├── static/
│   ├── staticfiles/
│   ├── backups/             # Backups de DB
│   └── manage.py
│
├── docs/                    # Solo docs importantes
│   ├── MANUAL_USUARIO_COMPLETO.md
│   ├── PRODUCTION_READY_FINAL.md
│   └── BUGS_CORREGIDOS_COMPLETO.md
│
├── tests_e2e/              # Tests E2E
│
├── requirements.txt
├── railway.toml
├── runtime.txt
├── README.md
└── CHECKLIST.md
```

---

## 💾 ESTIMACIÓN DE ESPACIO LIBERADO

```
_cleanup_backup_20251020/  : ~4-5 MB
_archive/                  : ~2-3 MB
.archived/                 : ~3-4 MB
Templates obsoletos        : ~500 KB
Scripts temporales         : ~100 KB
-----------------------------------
TOTAL ESTIMADO            : ~10-13 MB
```

---

## ⚡ EJECUCIÓN RÁPIDA

### Comando único para limpieza completa:
```bash
cd /Users/giulianozulatto/Proyectos/lino_saludable

# Eliminar carpetas grandes
rm -rf _cleanup_backup_20251020 _archive .archived

# Eliminar templates obsoletos
rm -rf src/gestion/templates/gestion/_backup_templates
rm -rf src/gestion/templates/gestion/_old
rm -rf src/gestion/templates/_obsolete_templates
rm -f src/gestion/templates/modules/productos/lista_productos_CORRUPTED.html
rm -f src/gestion/templates/gestion/dashboard_rentabilidad_old.html

# Eliminar scripts temporales
rm -f audit_production.py investigate_stock_bug.py test_e2e_manual.py
rm -f verify_dashboard_manual.py verify_dashboard_simple.py
rm -f commit_limpieza.sh migrate.sh

# Ver resultado
git status
```

---

## 🔍 VERIFICACIÓN POST-LIMPIEZA

```bash
# 1. Verificar que no rompimos nada
cd src
python manage.py check

# 2. Ejecutar tests
python manage.py test

# 3. Probar servidor
python manage.py runserver

# Si todo funciona:
git status
git add -A
git commit -m "🧹 Limpieza: Eliminar archivos obsoletos y duplicados

- Eliminadas carpetas de backup antiguas
- Eliminados templates obsoletos
- Eliminados scripts temporales
- Proyecto más limpio y mantenible
"
```

---

## 📚 DOCUMENTACIÓN A CONSOLIDAR

Actualmente hay ~30 archivos en `docs/`. Propuesta de consolidación:

### Mantener (10 archivos)
1. `MANUAL_USUARIO_COMPLETO.md` - Manual principal
2. `MANUAL_RESUMIDO.md` - Guía rápida
3. `PRODUCTION_READY_FINAL.md` - Deployment
4. `BUGS_CORREGIDOS_COMPLETO.md` - Historial bugs
5. `ESPECIFICACIONES_TECNICAS_HOSTING.md` - Hosting
6. `GUIA_TESTS_E2E.md` - Testing
7. `MANUAL_PARTE_2_INVENTARIO.md`
8. `MANUAL_PARTE_3_OPERACIONES.md`
9. `MANUAL_PARTE_4_METRICAS.md`
10. `MANUAL_PARTE_5_CONFIGURACION.md`

### Consolidar o Eliminar (~20 archivos)
- Archivos `ESTADO_*` antiguos → Un solo `ESTADO_ACTUAL.md`
- Archivos `FASE_*` → Consolidar en `ROADMAP.md`
- Múltiples análisis → Un solo `ANALISIS_SISTEMA.md`

---

**Siguiente paso:** Ejecutar la limpieza y verificar
