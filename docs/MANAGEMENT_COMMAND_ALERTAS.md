# Management Command: generar_alertas

## 📋 Descripción

Command de Django para generar alertas automáticas del sistema LINO. Permite ejecutar la generación de alertas de forma manual o programada vía cron jobs.

---

## 🚀 Uso Básico

### Generar todas las alertas para todos los usuarios
```bash
python manage.py generar_alertas
```

### Generar alertas para un usuario específico
```bash
python manage.py generar_alertas --usuario admin_giuli
```

### Generar solo alertas de stock
```bash
python manage.py generar_alertas --tipo stock
```

### Modo verbose (información detallada)
```bash
python manage.py generar_alertas --verbose
```

---

## 🎯 Opciones Disponibles

### `--usuario USERNAME`
Genera alertas solo para el usuario especificado.
- **Ejemplo**: `--usuario admin_giuli`
- **Default**: Todos los usuarios activos

### `--tipo TIPO`
Tipo de alertas a generar:
- `stock` - Alertas de stock bajo y agotado
- `vencimiento` - Productos próximos a vencer (TODO: requiere campo fecha_vencimiento)
- `rentabilidad` - Alertas de rentabilidad baja
- `stock_muerto` - Productos con rotación muy lenta
- `oportunidades` - Productos de alta rentabilidad
- `todas` - **(DEFAULT)** Genera todos los tipos

**Ejemplo**: `--tipo stock`

### `--verbose`
Muestra información detallada del proceso.
- Muestra cada tipo de alerta generada
- Útil para debugging

**Ejemplo**: `--verbose`

---

## 📊 Ejemplos de Uso

### 1. Generar todas las alertas (modo silencioso)
```bash
python manage.py generar_alertas
```

**Salida esperada**:
```
============================================================
  LINO - Generador de Alertas Automáticas
============================================================
👥 Generando para 1 usuarios activos
📋 Tipo de alertas: todas

✓ admin_giuli: 4 alertas generadas

============================================================
  ✅ Proceso completado
============================================================
📊 Total de alertas generadas: 4
👥 Usuarios procesados: 1
🎉 ¡Alertas generadas exitosamente!
```

### 2. Generar solo alertas de stock crítico
```bash
python manage.py generar_alertas --tipo stock
```

### 3. Generar todas las alertas con detalle
```bash
python manage.py generar_alertas --verbose
```

**Salida esperada**:
```
Procesando: admin_giuli
  • stock: 1 alertas
  • rentabilidad: 2 alertas
  • stock_muerto: 1 alertas
```

### 4. Generar alertas para un usuario específico
```bash
python manage.py generar_alertas --usuario admin_giuli --tipo todas --verbose
```

---

## ⏰ Automatización con Cron

### En Linux/macOS

Editar crontab:
```bash
crontab -e
```

Agregar línea para ejecutar diariamente a las 8:00 AM:
```bash
0 8 * * * cd /ruta/a/lino_saludable/src && /ruta/a/venv/bin/python manage.py generar_alertas >> /var/log/lino_alertas.log 2>&1
```

### Ejemplo con ruta completa
```bash
0 8 * * * cd /Users/giulianozulatto/Proyectos/lino_saludable/src && /Users/giulianozulatto/Proyectos/lino_saludable/venv/bin/python manage.py generar_alertas >> /tmp/lino_alertas.log 2>&1
```

### Frecuencias comunes

**Cada hora**:
```bash
0 * * * * cd /ruta/src && python manage.py generar_alertas
```

**Cada 6 horas**:
```bash
0 */6 * * * cd /ruta/src && python manage.py generar_alertas
```

**Diario a las 8 AM y 8 PM**:
```bash
0 8,20 * * * cd /ruta/src && python manage.py generar_alertas
```

**Solo días laborables a las 9 AM**:
```bash
0 9 * * 1-5 cd /ruta/src && python manage.py generar_alertas
```

---

## 🔧 Implementación Técnica

### Archivo
`src/gestion/management/commands/generar_alertas.py`

### Servicio utilizado
`gestion.services.alertas_service.AlertasService`

### Métodos llamados
- `generar_todas_alertas(usuario)` - Genera todos los tipos
- `generar_alertas_stock(usuario)` - Stock bajo/agotado
- `generar_alertas_vencimiento(usuario)` - Próximos a vencer
- `generar_alertas_rentabilidad(usuario)` - Rentabilidad baja
- `generar_alertas_stock_muerto(usuario)` - Rotación lenta
- `generar_alertas_oportunidades(usuario)` - Alta rentabilidad

---

## 🎨 Colores en Terminal

El comando utiliza `self.style` de Django para colorear la salida:
- ✅ Verde: Success
- ⚠️ Amarillo: Warning
- ❌ Rojo: Error

---

## 🐛 Troubleshooting

### Error: "Usuario X no encontrado"
**Causa**: El username no existe en la base de datos.

**Solución**: Verificar que el usuario existe:
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all().values_list('username', flat=True)
```

### No se generan alertas
**Posibles causas**:
1. Ya existen alertas no leídas del mismo tipo
2. No hay productos que cumplan las condiciones (stock bajo, etc.)
3. El usuario no tiene permisos suficientes

**Solución**: Ejecutar con `--verbose` para ver detalles:
```bash
python manage.py generar_alertas --verbose
```

---

## 📝 Logs

### Redirigir a archivo
```bash
python manage.py generar_alertas >> /var/log/lino_alertas.log 2>&1
```

### Ver logs en tiempo real
```bash
tail -f /var/log/lino_alertas.log
```

---

## 🔄 Integración con otras herramientas

### Celery (Task Queue)
```python
# tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def generar_alertas_task():
    call_command('generar_alertas', tipo='todas')
```

### Django-cron
```python
# cron.py
from django_cron import CronJobBase, Schedule

class GenerarAlertasCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # cada hora
    
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'gestion.generar_alertas_cron'
    
    def do(self):
        call_command('generar_alertas')
```

---

## ✅ Testing

### Test manual
```bash
# 1. Limpiar alertas existentes (opcional)
python manage.py shell
>>> from gestion.models import Alerta
>>> Alerta.objects.all().delete()

# 2. Generar alertas
python manage.py generar_alertas --verbose

# 3. Verificar en la UI
# http://localhost:8000/gestion/alertas/
```

---

**Creado**: 5 de noviembre de 2025  
**Versión**: 1.0  
**Autor**: GitHub Copilot
