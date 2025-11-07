# 🎭 Guía de Tests E2E con Playwright - Sistema LINO

## 📋 Resumen

Esta guía explica cómo ejecutar tests End-to-End (E2E) del sistema LINO usando Playwright.

---

## ✅ Configuración Completada

### Instalación
```bash
# Playwright y dependencias ya instaladas
pip install playwright pytest-playwright pytest-django

# Browsers instalados
playwright install chromium
```

### Estructura de Archivos
```
lino_saludable/
├── pytest.ini                      # Configuración de pytest
├── conftest.py                     # Fixtures globales
├── test_e2e_manual.py             # Tests E2E manuales (sin pytest)
└── tests_e2e/                      # Suite de tests E2E
    ├── __init__.py
    ├── conftest.py                 # Fixtures específicas E2E
    └── test_critical_flows.py      # Tests de flujos críticos
```

---

## 🚀 Cómo Ejecutar Tests E2E

### Opción 1: Tests Manuales (Recomendado)

**Ventajas**: Simple, sin problemas de async/sync, fácil debugging

**Pasos**:

1. **Levantar servidor Django**:
```bash
cd src
python manage.py runserver 8000
```

2. **En otra terminal, ejecutar tests**:
```bash
python test_e2e_manual.py
```

3. **Presionar ENTER** cuando el script lo pida

4. **Ver resultados**:
```
================================================================================
  TESTS E2E - SISTEMA LINO
================================================================================

✅ Login y redirección
✅ Dashboard carga
✅ Lista productos accesible
✅ Lista MPs accesible
✅ Lista ventas accesible
✅ Lista compras accesible
✅ Lista ajustes accesible

================================================================================
  RESUMEN FINAL - TESTS E2E
================================================================================

📊 Tests ejecutados: 7
✅ Tests pasando: 7
❌ Tests fallando: 0
📈 Porcentaje: 100.0%
```

---

### Opción 2: Tests con Pytest (Avanzado)

⚠️ **Nota**: Esta opción tiene problemas conocidos de async/sync con Django ORM.

**Si quieres intentarlo**:

```bash
pytest tests_e2e/test_critical_flows.py -v
```

**Problema conocido**:
```
SynchronousOnlyOperation: You cannot call this from an async context
```

**Solución futura**: Usar `pytest-asyncio` o `sync_to_async` wrappers.

---

## 📝 Tests Implementados

### 1. Test de Login (`test_login`)
- Navega a `/admin/login/`
- Llena credenciales
- Verifica redirección exitosa

### 2. Test de Dashboard (`test_dashboard`)
- Navega a `/gestion/`
- Verifica carga sin errores 500/404

### 3. Test Lista de Productos (`test_productos_lista`)
- Navega a `/gestion/productos/`
- Verifica contenido presente

### 4. Test Lista de Materias Primas (`test_materias_primas_lista`)
- Navega a `/gestion/materias-primas/`
- Verifica accesibilidad

### 5. Test Lista de Ventas (`test_ventas_lista`)
- Navega a `/gestion/ventas/`
- Verifica carga correcta

### 6. Test Lista de Compras (`test_compras_lista`)
- Navega a `/gestion/compras/`
- Verifica accesibilidad

### 7. Test Lista de Ajustes (`test_ajustes_lista`)
- Navega a `/gestion/ajustes/`
- Verifica funcionalidad

---

## 🔧 Personalizar Tests

### Agregar Nuevo Test

Editar `test_e2e_manual.py`:

```python
def test_mi_nueva_funcionalidad(page):
    """TEST X: Descripción."""
    print_header("TEST X: Mi Nueva Funcionalidad")
    
    try:
        # Tu código aquí
        page.goto(f"{BASE_URL}/mi-url/")
        page.wait_for_load_state('networkidle')
        
        # Interacciones
        page.click('button#mi-boton')
        page.fill('input[name="campo"]', 'valor')
        
        # Verificaciones
        title = page.title()
        success = "error" not in title.lower()
        
        print_test("Mi test", success)
        return success
    except Exception as e:
        print_test("Mi test", False, f"Error: {str(e)}")
        return False
```

Luego agregar a `main()`:

```python
resultados['Mi Test'] = test_mi_nueva_funcionalidad(page)
```

---

## 🎯 Selectores Útiles

### Formularios
```python
# Por nombre
page.fill('input[name="username"]', 'valor')

# Por ID
page.click('#submit-button')

# Por tipo
page.fill('input[type="email"]', 'test@example.com')

# Por texto
page.click('button:has-text("Guardar")')
```

### Navegación
```python
# Ir a URL
page.goto('http://127.0.0.1:8000/gestion/')

# Esperar carga
page.wait_for_load_state('networkidle')

# Esperar selector
page.wait_for_selector('#elemento')

# Esperar timeout
page.wait_for_timeout(1000)  # 1 segundo
```

### Verificaciones
```python
# Verificar URL
assert '/gestion/' in page.url

# Verificar título
assert 'Dashboard' in page.title()

# Verificar contenido
assert 'Productos' in page.content()

# Verificar elemento visible
assert page.is_visible('#mi-elemento')
```

---

## 📊 Modo Headed (Ver Browser)

Para ver el browser mientras se ejecutan tests:

Editar `test_e2e_manual.py`, cambiar:

```python
# De:
browser = p.chromium.launch(headless=True)

# A:
browser = p.chromium.launch(headless=False, slow_mo=500)
```

- `headless=False`: Muestra el browser
- `slow_mo=500`: Ralentiza las acciones (ms)

---

## 🐛 Debugging

### Ver Screenshots

Agregar en tu test:

```python
# Tomar screenshot
page.screenshot(path='debug_screenshot.png')
```

### Ver HTML
```python
# Guardar HTML
with open('debug.html', 'w') as f:
    f.write(page.content())
```

### Pausar Ejecución
```python
# En modo headed, pausa para inspeccionar
page.pause()
```

---

## 📋 Checklist Pre-Ejecución

Antes de ejecutar tests E2E:

- [ ] Servidor Django corriendo (`python manage.py runserver 8000`)
- [ ] Base de datos migrada (`python manage.py migrate`)
- [ ] Usuario admin creado (opcional - tests crean su propio usuario)
- [ ] Chromium instalado (`playwright install chromium`)
- [ ] Dependencias instaladas (`pip install playwright pytest-playwright`)

---

## 🎓 Recursos Adicionales

### Documentación Oficial
- [Playwright Python](https://playwright.dev/python/)
- [Selectores CSS](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [pytest-django](https://pytest-django.readthedocs.io/)

### Ejemplos de Selectores
```python
# Tag
page.click('button')

# Clase
page.click('.btn-primary')

# ID
page.click('#submit')

# Atributo
page.click('[data-test="submit"]')

# Combinado
page.click('button.btn-primary#submit')

# Texto
page.click('text=Guardar')

# XPath
page.click('xpath=//button[text()="Guardar"]')
```

---

## ✅ Estado Actual

**Configuración**: ✅ COMPLETADA  
**Tests Implementados**: 7/7  
**Framework**: Playwright + Python Sync API  
**Browsers**: Chromium instalado  

**Próximos Pasos**:
1. Ejecutar tests manualmente para verificar
2. Agregar más tests según necesidades
3. Integrar a CI/CD (opcional)

---

**Última Actualización**: 7 de noviembre de 2025  
**Versión Playwright**: 1.55.0  
**Python**: 3.13.5
