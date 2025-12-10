# 📥 GUÍA DETALLADA: BACKUP DE RAILWAY

**Fecha:** 9 de Diciembre 2025  
**Usuario:** Cliente (no técnico)  
**Tiempo estimado:** 10 minutos

---

## 🎯 ¿QUÉ ES UN BACKUP?

Un **backup** (o copia de seguridad) es como una **foto de todos tus datos** en un momento específico.

**¿Para qué sirve?**
- 🔄 Si algo sale mal, podés volver a ese punto
- 💾 Proteger información de clientes, ventas, productos
- 🛡️ Seguridad ante errores o fallos técnicos

**Ejemplo:** 
- Hoy (9 dic) hacés backup → Captura todos tus datos
- Mañana (10 dic) borrás algo por error
- Restaurás backup de ayer → Recuperás lo que borraste

---

## 📊 CONCEPTOS IMPORTANTES

### **"Retención: 7-30 días"**

**¿Qué significa?**
- Es **cuánto tiempo Railway GUARDA** tus backups automáticos
- **7 días** = Railway mantiene los últimos 7 backups diarios
- **30 días** = Railway mantiene los últimos 30 backups diarios

**Ejemplo con 7 días:**
```
Hoy: 9 dic → Backup del 9 dic
Mañana: 10 dic → Backups del 9 y 10 dic
...
Día 7: 15 dic → Backups del 9, 10, 11, 12, 13, 14, 15 dic
Día 8: 16 dic → Backups del 10, 11, 12, 13, 14, 15, 16 dic
                (el del 9 dic se BORRA automáticamente)
```

**¿Cuál elegir?**
- **7 días:** Suficiente para mayoría de casos, más barato
- **30 días:** Más seguridad, pero más caro

**Recomendación para Lino:** 7 días es perfecto para empezar

---

### **"Setup: 1-2 horas"**

**¿Qué significa?**
- Es el **tiempo total** que lleva configurar TODO el sistema de backups
- **NO es 1-2 horas para VOS**, es para el desarrollador (yo)

**Desglose del tiempo:**

| Tarea | Tiempo | Quién |
|-------|--------|-------|
| 1. Activar Railway Backups | 5 min | **VOS** (hoy) |
| 2. Crear script de backup manual | 40 min | Desarrollador |
| 3. Probar que funciona | 10 min | Desarrollador |
| 4. Documentar proceso | 15 min | Desarrollador |
| 5. Configurar alertas | 20 min | Desarrollador |
| **TOTAL** | **90 min** | **Mayormente dev** |

**Para vos HOY solo necesitás:** 5-10 minutos (activar Railway Backups)

---

## 📥 MÉTODO 1: BACKUP MANUAL VÍA RAILWAY DASHBOARD

### **PASO 1: Acceder a Railway**

1. **Abrí tu navegador:** Chrome, Firefox, Safari
2. **Andá a:** https://railway.app
3. **Login:**
   - Si usaste GitHub: "Sign in with GitHub"
   - Si usaste Email: Ingresá tu email y contraseña

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────┐
│  Railway                    👤  │
├─────────────────────────────────┤
│                                 │
│  Your Projects                  │
│                                 │
│  ┌───────────────────────┐     │
│  │ 📦 lino_saludable     │     │
│  │ Active - 5 min ago    │     │
│  └───────────────────────┘     │
│                                 │
└─────────────────────────────────┘
```

**✅ Verificación:** Ves tu proyecto "lino_saludable" (o similar)

---

### **PASO 2: Abrir tu Proyecto**

1. **Click en el proyecto** "lino_saludable"
2. Se abre una pantalla con "servicios"

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────────────┐
│ lino_saludable              Settings ⚙️  │
├─────────────────────────────────────────┤
│                                         │
│  Services:                              │
│                                         │
│  ┌─────────────┐  ┌──────────────┐    │
│  │ 🌐 web      │  │ 🐘 postgres  │    │
│  │ (Python)    │  │ (Database)   │    │
│  └─────────────┘  └──────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

**✅ Verificación:** Ves 2 servicios:
- `web` (tu aplicación Django)
- `postgres` o `postgresql` (tu base de datos)

---

### **PASO 3: Entrar a PostgreSQL**

1. **Click en el servicio "postgres"** 🐘
2. Se abre la configuración de la base de datos

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────────────┐
│ PostgreSQL                               │
├─────────────────────────────────────────┤
│ Variables │ Settings │ Metrics │ Data  │ ← Estas pestañas
├─────────────────────────────────────────┤
│                                         │
│  Database Information:                  │
│  Name: railway                          │
│  Size: 45.2 MB                          │
│  Tables: 28                             │
│                                         │
└─────────────────────────────────────────┘
```

**✅ Verificación:** 
- Título dice "PostgreSQL" o "Postgres"
- Ves pestañas arriba: Variables, Settings, Metrics, Data

---

### **PASO 4: Ir a la Pestaña "Data"**

1. **Click en la pestaña "Data"** (arriba)
2. Vas a ver tus tablas (gestion_producto, gestion_venta, etc.)

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────────────┐
│ Data                    [+ Query] [⬇️ Export] │ ← Acá!
├─────────────────────────────────────────┤
│                                         │
│  Tables:                                │
│  ✓ auth_user            (15 rows)      │
│  ✓ gestion_producto     (45 rows)      │
│  ✓ gestion_venta        (128 rows)     │
│  ✓ gestion_ventadetalle (256 rows)     │
│  ...                                    │
│                                         │
└─────────────────────────────────────────┘
```

**✅ Verificación:** 
- Ves lista de tablas
- Cada tabla muestra cantidad de filas (rows)

---

### **PASO 5: Exportar Backup**

1. **Arriba a la derecha** buscá botón **"Export"** ⬇️ o **"Download"**
2. **Click en "Export"**
3. Railway va a generar el backup (puede tardar 10-30 segundos)
4. Se descarga automáticamente un archivo

**Nombres posibles del archivo:**
- `railway_backup_2025_12_09.sql`
- `postgres_export.sql`
- `lino_saludable_backup.dump`

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────┐
│ Exporting database...           │
│ ████████████░░░░░░░ 65%         │
│                                 │
│ This may take a moment...       │
└─────────────────────────────────┘

(Luego se descarga automáticamente)
```

**✅ Verificación:** 
- Archivo descargado en tu carpeta "Descargas" o "Downloads"
- **Tamaño:** Mínimo 10 KB (si tenés pocos datos), puede ser varios MB
- **Formato:** `.sql` o `.dump`

---

### **PASO 6: VERIFICAR que el Backup está OK**

#### **Verificación Básica (Fácil):**

1. **Abrí tu carpeta de Descargas**
2. **Buscá el archivo** recién descargado
3. **Click derecho → Obtener información** (Mac) o **Propiedades** (Windows)
4. **Mirá el tamaño:**
   - ✅ **> 10 KB:** Probablemente OK
   - ✅ **> 100 KB:** Definitivamente OK
   - ❌ **< 5 KB:** Puede estar vacío o roto

5. **Abrí el archivo con un editor de texto** (TextEdit, Notepad, VS Code)
6. **Primeras líneas deberían decir:**
   ```sql
   --
   -- PostgreSQL database dump
   --
   
   -- Dumped from database version 14.x
   -- Dumped by pg_dump version 14.x
   
   SET statement_timeout = 0;
   ...
   ```

**✅ BACKUP OK si ves:**
- Líneas que empiezan con `--` (comentarios SQL)
- Comandos como `CREATE TABLE`, `INSERT INTO`, etc.
- Nombres de tus tablas: `gestion_producto`, `gestion_venta`

---

#### **Verificación Avanzada (Opcional):**

Si querés estar 100% seguro:

```bash
# En terminal (Mac/Linux):
grep -c "INSERT INTO" ~/Downloads/railway_backup*.sql

# Resultado esperado:
# Número > 0 (significa que tiene datos)
```

O buscá manualmente en el archivo:
- `INSERT INTO gestion_producto` → Debe aparecer varias veces
- `INSERT INTO gestion_venta` → Debe aparecer si tenés ventas

---

### **PASO 7: Guardar el Backup de Forma Segura**

1. **Renombralo** con fecha clara:
   ```
   backup_lino_20251209_pre_deploy.sql
   ```

2. **Copialo a 2 lugares:**
   - 📁 Carpeta en tu computadora: `~/Backups/lino_saludable/`
   - ☁️ Nube: Google Drive, Dropbox, iCloud

3. **Verificá que se copió bien:**
   - Tamaño igual en ambos lugares
   - Fecha de modificación es hoy

**✅ Verificación final:** 
- Tenés el archivo en 3 lugares:
  1. Descargas (original)
  2. Carpeta local de backups
  3. Nube (Drive/Dropbox)

---

## 📥 MÉTODO 2: BACKUP VÍA RAILWAY CLI

**⚠️ Método alternativo si no encontrás botón "Export"**

### **Prerrequisitos:**

1. Tener instalado Railway CLI (comando de terminal)
2. Estar logueado en Railway desde terminal

---

### **PASO 1: Instalar Railway CLI**

```bash
# En tu terminal (Mac/Linux):
npm install -g @railway/cli

# O con Homebrew (Mac):
brew install railway
```

**✅ Verificación:**
```bash
railway --version
# Debería mostrar: Railway CLI v3.x.x
```

---

### **PASO 2: Login en Railway**

```bash
railway login
```

1. Se abre tu navegador
2. Autorizás la Railway CLI
3. Volvés a la terminal

**✅ Verificación:**
```bash
railway whoami
# Debería mostrar tu email/usuario
```

---

### **PASO 3: Conectar al Proyecto**

```bash
cd ~/Proyectos/lino_saludable
railway link
```

1. Te muestra lista de proyectos
2. Seleccionás "lino_saludable"
3. Se conecta

**✅ Verificación:**
```bash
railway status
# Debería mostrar info de tu proyecto
```

---

### **PASO 4: Hacer Backup**

```bash
# Opción 1: Export directo
railway run pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Opción 2: Conectar y exportar
railway connect postgres
# (Abre conexión a la DB)
\copy (SELECT * FROM gestion_producto) TO 'productos.csv' CSV HEADER;
\q
```

**✅ Verificación:**
```bash
ls -lh backup_*.sql
# Debería mostrar el archivo con tamaño
```

---

## 🔄 ACTIVAR BACKUPS AUTOMÁTICOS EN RAILWAY

**⚠️ IMPORTANTE:** Esto requiere un plan PAGO de Railway

### **PASO 1: Verificar tu Plan Actual**

1. Railway Dashboard → Click en tu foto de perfil (arriba derecha)
2. Click en "Billing" o "Account Settings"
3. Mirá tu plan actual:
   - **Developer (Free):** $0/mes - NO tiene backups automáticos
   - **Hobby ($5/mes):** Puede tener backups básicos
   - **Pro ($20/mes):** Backups automáticos completos

---

### **PASO 2: Upgrade de Plan (Si es necesario)**

**⚠️ Decisión comercial:** Discutir con tu hermana antes

1. Railway Dashboard → Account Settings → Billing
2. Click en "Upgrade Plan"
3. Elegir plan:
   - **Hobby ($5/mes):** OK para comenzar
   - **Pro ($20/mes):** Mejor protección

4. Ingresar tarjeta de crédito
5. Confirmar upgrade

---

### **PASO 3: Activar Backups Automáticos**

1. Railway Dashboard → Tu proyecto → PostgreSQL
2. Click en **"Settings"** (pestaña)
3. Buscá sección **"Backups"** o **"Data Retention"**
4. **Enable "Automated Backups"**
5. Configurar:
   - **Frequency:** Daily (Diario)
   - **Time:** 03:00 AM (3 de la mañana)
   - **Retention:** 7 days (o 30 days si tenés Pro)
6. **Save Settings**

**🖼️ Lo que vas a ver:**
```
┌─────────────────────────────────────────┐
│ Backup Settings                         │
├─────────────────────────────────────────┤
│                                         │
│ ☑ Enable Automated Backups              │
│                                         │
│ Frequency: [Dropdown: Daily ▼]         │
│ Time:      [Input: 03:00] (UTC)        │
│ Retention: [Dropdown: 7 days ▼]        │
│                                         │
│             [Cancel]  [Save]            │
│                                         │
└─────────────────────────────────────────┘
```

**✅ Verificación:**
- Toggle "Automated Backups" está en ON (azul/verde)
- Dice "Frequency: Daily"
- Dice "Retention: 7 days" (o lo que elegiste)

---

### **PASO 4: Verificar que Funciona**

**Esperar 24 horas** (hasta el próximo backup)

Luego:

1. Railway Dashboard → PostgreSQL → Settings → Backups
2. Deberías ver una lista de backups:
   ```
   📦 Backup - Dec 10, 2025 03:00 AM (45.2 MB)
   📦 Backup - Dec 9, 2025 03:00 AM (44.8 MB)
   ```

3. Click en un backup → Opciones:
   - **Download:** Descargar
   - **Restore:** Restaurar (¡CUIDADO! sobrescribe DB actual)

**✅ Verificación exitosa:**
- Al día siguiente ves backup nuevo en la lista
- Tamaño es consistente (45-50 MB aproximadamente)

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### **Problema 1: No veo botón "Export"**

**Soluciones:**
1. Verificar que estás en la pestaña "Data" (no "Settings")
2. Probar desde otro navegador (a veces Chrome no lo muestra)
3. Usar Railway CLI (Método 2 arriba)
4. Contactar soporte de Railway

---

### **Problema 2: Backup muy chico (< 5 KB)**

**Causas:**
- Base de datos vacía (recién creada)
- Error en la exportación

**Solución:**
1. Verificar que tenés datos en Railway:
   - Ir a "Data" tab → Ver tablas
   - Debería haber rows (filas) en las tablas
2. Reintentar export
3. Probar con Railway CLI

---

### **Problema 3: "Permission Denied" o Error 403**

**Causas:**
- No tenés permisos de admin en el proyecto
- Session expirada

**Solución:**
1. Verificar que sos owner o admin del proyecto
2. Logout y login nuevamente en Railway
3. Limpiar cache del navegador
4. Reintentar

---

### **Problema 4: Archivo .dump no se puede abrir**

**Explicación:**
- `.dump` es formato binario comprimido
- NO se puede leer como texto normal

**Solución:**
- Es NORMAL, está bien así
- Para verificarlo necesitás usar `pg_restore` (comando avanzado)
- Si querés texto legible, pedí formato `.sql` al exportar

---

## ✅ CHECKLIST FINAL

Después de hacer el backup, verificá:

- [ ] Archivo descargado existe
- [ ] Tamaño > 10 KB (preferiblemente > 100 KB)
- [ ] Fecha de modificación es HOY
- [ ] Nombre tiene la fecha (ej: backup_20251209.sql)
- [ ] Copiado en 2 lugares (local + nube)
- [ ] Al abrirlo con editor de texto se ve SQL (si es .sql)
- [ ] Guardaste la ubicación para encontrarlo después

---

## 📞 ¿NECESITÁS AYUDA?

Si algo no funciona:

1. **Capturá pantalla** de lo que estás viendo
2. **Anotá el mensaje de error** exacto
3. **Contactame** y te ayudo en vivo

---

## 🎯 RESUMEN EJECUTIVO

**Para hacer backup manual HOY (antes del deploy):**

1. ✅ Ir a https://railway.app
2. ✅ Login
3. ✅ Abrir proyecto "lino_saludable"
4. ✅ Click en "PostgreSQL"
5. ✅ Pestaña "Data"
6. ✅ Botón "Export"
7. ✅ Descargar archivo
8. ✅ Verificar tamaño > 10 KB
9. ✅ Renombrar: `backup_lino_20251209_pre_deploy.sql`
10. ✅ Copiar a Drive/Dropbox

**Tiempo total:** 5-10 minutos

**Después del backup confirmado → Procedemos con DEPLOY** 🚀

---

**¿Todo claro? ¿Alguna duda?** 

Cuando tengas el backup listo, avisame y seguimos con el deploy 👍
