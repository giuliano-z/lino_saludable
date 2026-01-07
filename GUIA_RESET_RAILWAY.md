# 🚨 GUÍA: RESETEAR BASE DE DATOS DE PRODUCCIÓN (RAILWAY)

**Fecha:** 7 de Enero 2026  
**Objetivo:** Eliminar TODOS los datos y empezar desde cero en enero  
**⚠️  ADVERTENCIA:** Esta operación NO se puede deshacer

---

## 📋 ¿QUÉ SE VA A ELIMINAR?

### ❌ **Se eliminará TODO:**
- Todas las ventas y sus detalles
- Todas las compras y sus detalles
- Todos los productos
- Todas las materias primas
- Todas las recetas
- Todos los lotes
- Todas las alertas
- Todos los movimientos de inventario
- Todo el historial de costos y precios
- Todos los ajustes de inventario
- Todos los usuarios EXCEPTO los 2 principales

### ✅ **Se mantendrá SOLO:**
- **Usuario 1:** `sister_emprendedora` (Password: `SisterLino2025!`)
- **Usuario 2:** `el_super_creador` (Password: `CreadorLino2025!`)

---

## 🚀 PASOS PARA EJECUTAR EN RAILWAY

### **OPCIÓN 1: Desde Railway CLI (Recomendada)**

#### 1. Instalar Railway CLI (si no lo tienes)
```bash
# macOS/Linux
brew install railway

# O con npm
npm install -g @railway/cli
```

#### 2. Login a Railway
```bash
railway login
```

#### 3. Conectar al proyecto
```bash
cd /Users/giulianozulatto/Proyectos/lino_saludable
railway link
# Selecciona: lino_saludable (o el nombre de tu proyecto)
```

#### 4. Abrir shell de Railway
```bash
railway run bash
```

#### 5. Ejecutar el comando de reset
```bash
# Primero ver qué se eliminará (simulación)
python src/manage.py reset_production --dry-run

# Si estás seguro, ejecutar el reset real
python src/manage.py reset_production --confirm
```

#### 6. Confirmar la operación
Cuando te pida confirmación, escribe exactamente:
```
RESETEAR PRODUCCION
```

---

### **OPCIÓN 2: Desde Railway Dashboard**

#### 1. Ir a Railway Dashboard
```
https://railway.app/
```

#### 2. Seleccionar tu proyecto
- Busca: `lino_saludable` o `web-production-b0ad1`

#### 3. Abrir la terminal del servicio
- Click en el servicio "web"
- Click en la pestaña "Shell" o "Terminal"

#### 4. Navegar al directorio correcto
```bash
cd src
```

#### 5. Ejecutar el comando
```bash
# Ver simulación primero
python manage.py reset_production --dry-run

# Ejecutar reset
python manage.py reset_production --confirm
```

#### 6. Confirmar escribiendo:
```
RESETEAR PRODUCCION
```

---

## ✅ VERIFICACIÓN POST-RESET

### 1. Verificar que el sistema esté limpio
```bash
# En Railway shell:
python src/manage.py shell

# En el shell de Python:
from gestion.models import Producto, MateriaPrima, Venta, Compra
from django.contrib.auth.models import User

print(f"Productos: {Producto.objects.count()}")  # Debe ser 0
print(f"Materias primas: {MateriaPrima.objects.count()}")  # Debe ser 0
print(f"Ventas: {Venta.objects.count()}")  # Debe ser 0
print(f"Compras: {Compra.objects.count()}")  # Debe ser 0
print(f"Usuarios: {User.objects.count()}")  # Debe ser 2

# Ver usuarios
for u in User.objects.all():
    print(f"Usuario: {u.username} - {u.email}")
```

### 2. Verificar login en el navegador
```
URL: https://web-production-b0ad1.up.railway.app/admin/

Usuario: sister_emprendedora
Password: SisterLino2025!
```

---

## 📝 SIGUIENTES PASOS DESPUÉS DEL RESET

### 1. **Cargar Productos**
- Ve a: Productos → Agregar nuevo
- Ingresa cada producto con:
  - Nombre
  - Precio de enero 2026
  - Stock inicial = 0 (se actualizará con producción)
  - Categoría
  - Stock mínimo

### 2. **Cargar Materias Primas**
- Ve a: Materias Primas → Agregar nueva
- Ingresa cada materia prima con:
  - Nombre
  - Costo unitario de enero 2026
  - Stock actual = 0 (se actualizará con compras)
  - Unidad de medida
  - Proveedor

### 3. **Registrar Compras de Enero**
- Ve a: Compras → Nueva compra
- Registra las compras reales de enero
- El sistema actualizará automáticamente el stock de materias primas

### 4. **Producir Productos**
- Ve a: Producción → Producir
- Selecciona producto y cantidad
- El sistema descontará materias primas y sumará stock de productos

### 5. **Comenzar a Vender**
- Ve a: Ventas → Nueva venta
- Registra las ventas normalmente
- Las métricas se empezarán a generar automáticamente

---

## 🔄 ALTERNATIVA: RESET SIN ELIMINAR PRODUCTOS/MATERIAS PRIMAS

Si prefieres mantener la estructura de productos y solo limpiar transacciones:

```bash
# Usa el otro comando:
python src/manage.py reset_inventory --dry-run
python src/manage.py reset_inventory

# Este comando:
# ❌ Elimina: ventas, compras, alertas, movimientos, historiales
# ✅ Mantiene: productos y materias primas (con stock en 0)
# ✅ Mantiene: todos los usuarios
```

---

## 🆘 TROUBLESHOOTING

### Problema: "Command not found"
**Solución:** Asegúrate de estar en el directorio correcto:
```bash
cd src
python manage.py reset_production --dry-run
```

### Problema: "Import error: No module named gestion"
**Solución:** Verifica que estés en el proyecto correcto:
```bash
ls -la  # Debe mostrar manage.py
```

### Problema: Railway CLI no conecta
**Solución:** 
```bash
railway logout
railway login
railway link
```

### Problema: "This command requires --confirm"
**Solución:** Debes agregar el flag explícitamente:
```bash
python manage.py reset_production --confirm
```

---

## 📞 CONTACTO EN CASO DE PROBLEMAS

Si algo sale mal:
1. NO ejecutes más comandos
2. Copia el error exacto que apareció
3. Contacta al desarrollador con el mensaje de error

---

## ⚠️ RECORDATORIO FINAL

- ✅ Haz un backup si tienes algo importante (aunque sea screenshot)
- ✅ Asegúrate de estar en el ambiente correcto (Railway = producción)
- ✅ Verifica que los usuarios se mantengan después del reset
- ✅ Prueba el login antes de cargar todo de nuevo

**¿Listo para ejecutar?** 🚀
