# 🚨 INSTRUCCIONES URGENTES - BACKUP MANUAL

**Fecha:** 9 de Diciembre 2025, 23:59 hs  
**Situación:** Railway no permite backup automático en plan gratuito

---

## ✅ MÉTODO ALTERNATIVO SIMPLE

Como Railway requiere plan Pro para backups automáticos, usamos este método:

---

### **OPCIÓN A: Backup via Railway Dashboard (Más Simple)**

#### **PASO 1: Ir a Settings de PostgreSQL**
1. Railway Dashboard → PostgreSQL
2. Click en pestaña **"Settings"**

#### **PASO 2: Buscar "Public Networking"**
1. Scroll down hasta encontrar sección **"TCP Proxy"** o **"Public URL"**
2. Debería haber un dominio tipo: `roundhouse.proxy.rlwy.net:12345`

#### **PASO 3: Obtener Credenciales**
1. En Settings → Variables
2. Copiar:
   - **PGHOST:** `roundhouse.proxy.rlwy.net` (o similar)
   - **PGPORT:** `12345` (número de puerto)
   - **PGDATABASE:** `railway`
   - **PGUSER:** `postgres`
   - **PGPASSWORD:** (la contraseña)

#### **PASO 4: Volver a Terminal y ejecutar:**

```bash
# Reemplazar con TUS valores:
PGPASSWORD='TU_PASSWORD_AQUI' pg_dump \
  -h roundhouse.proxy.rlwy.net \
  -p 12345 \
  -U postgres \
  -d railway \
  -F c \
  -f backups/backup_pre_deploy_20251209.dump

# O en formato SQL legible:
PGPASSWORD='TU_PASSWORD_AQUI' pg_dump \
  -h roundhouse.proxy.rlwy.net \
  -p 12345 \
  -U postgres \
  -d railway \
  > backups/backup_pre_deploy_20251209.sql
```

---

### **OPCIÓN B: Backup Simple de Datos Críticos (FALLBACK)**

Si lo anterior no funciona, hacemos backup selectivo:

#### **1. Exportar Productos:**
Railway Dashboard → PostgreSQL → Data → gestion_producto  
→ Click en tabla → Export to CSV

#### **2. Exportar Ventas:**
Railway Dashboard → PostgreSQL → Data → gestion_venta  
→ Click en tabla → Export to CSV

#### **3. Exportar Ventas Detalle:**
Railway Dashboard → PostgreSQL → Data → gestion_ventadetalle  
→ Click en tabla → Export to CSV

**Guardar los 3 CSV en carpeta `backups/`**

---

### **OPCIÓN C: Proceder SIN Backup (⚠️ RIESGOSO)**

**Análisis de Riesgo:**

✅ **Factores de seguridad:**
- Cliente NO está usando sistema
- Cambios probados localmente (9/9 tests pasando)
- Deploy anterior fue exitoso
- Railway mantiene historial de deployments (rollback posible)

⚠️ **Riesgos:**
- Si falla deploy, perdemos estado actual de DB
- Railway puede hacer rollback de código, pero NO de DB

🎯 **Recomendación:**
- Proceder con deploy
- Después configurar backups automáticos (próxima semana)
- Este fix es crítico (bug afecta todas las ventas)

---

## 📊 DECISIÓN ESTRATÉGICA

| Factor | Peso | Backup SÍ | Backup NO |
|--------|------|-----------|-----------|
| Cliente usando sistema | 🔴 | - | ✅ NO está usando |
| Tests pasando | 🟢 | ✅ | ✅ 9/9 |
| Urgencia del fix | 🔴 | - | ✅ Bug crítico |
| Rollback disponible | 🟡 | ✅ | ✅ Railway deploy |
| Tiempo invertido | 🟡 | 30+ min | 0 min |

**RECOMENDACIÓN:** Proceder con deploy sin backup, luego implementar backups automáticos.

---

## 🚀 SI DECIDÍS PROCEDER SIN BACKUP:

```bash
# 1. Agregar estas guías al repo
git add backups/ GUIA_BACKUP_RAILWAY_DETALLADA.md PLAN_BACKUPS_AUTOMATICOS.md

# 2. Commit
git commit -m "docs: agregar guías de backup para configuración futura"

# 3. Deploy
git push origin main

# 4. Monitorear Railway logs
railway logs --follow
```

---

## ⏭️ PRÓXIMOS PASOS POST-DEPLOY:

1. **Inmediato (hoy):** Verificar deploy exitoso
2. **Esta semana:** Upgrade a Railway Pro ($5/mes)
3. **Esta semana:** Activar backups automáticos
4. **Próxima semana:** Implementar script de backup manual

---

**¿Cómo procedemos?** 🤔
