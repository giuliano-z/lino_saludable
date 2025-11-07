#!/usr/bin/env python3
"""
🔍 VERIFICACIÓN SIMPLE - DASHBOARD PRODUCCIÓN
Abre el navegador automáticamente y te muestra el dashboard

Ejecutar:
    python verify_dashboard_simple.py
"""

from playwright.sync_api import sync_playwright
import time


BASE_URL = "https://web-production-b0ad1.up.railway.app"
USERNAME = "el_super_creador"
PASSWORD = "tiSrsgz2nBqrVLA"


print("=" * 80)
print("  🔍 ABRIENDO DASHBOARD EN NAVEGADOR")
print("=" * 80)
print(f"\n📍 URL: {BASE_URL}/gestion/")
print(f"👤 Usuario: {USERNAME}")
print(f"🔑 Password: {PASSWORD}\n")
print("⏳ Abriendo navegador en 3 segundos...")
time.sleep(3)

try:
    with sync_playwright() as p:
        # Abrir navegador visible
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        print("\n✅ Navegador abierto")
        print("📄 Cargando página de login...")
        
        # Ir a login
        page.goto(f"{BASE_URL}/admin/login/", timeout=30000)
        page.wait_for_load_state('networkidle')
        
        print("✅ Login page cargada")
        print("🔐 Iniciando sesión...")
        
        # Login
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_load_state('networkidle')
        
        print("✅ Login exitoso")
        print("📊 Cargando dashboard...")
        
        # Ir al dashboard
        page.goto(f"{BASE_URL}/gestion/", timeout=30000)
        page.wait_for_load_state('networkidle')
        time.sleep(3)  # Esperar elementos dinámicos
        
        print("✅ Dashboard cargado\n")
        print("=" * 80)
        print("  📋 VERIFICA VISUALMENTE:")
        print("=" * 80)
        print("\n1. ¿Ves tarjetas con KPIs? (Ventas, Compras, Stock)")
        print("2. ¿Hay gráficos? (barras, líneas, etc.)")
        print("3. ¿Funciona la navegación? (links a Productos, MPs, etc.)")
        print("4. ¿Los estilos se ven bien? (colores, diseño)")
        print("\n📸 Tomando screenshot...")
        
        # Screenshot
        page.screenshot(path='dashboard_screenshot.png', full_page=True)
        print("✅ Screenshot guardado: dashboard_screenshot.png")
        
        print("\n⏰ El navegador permanecerá abierto por 60 segundos")
        print("   Explora el dashboard libremente...")
        print("   Presiona Ctrl+C para cerrar antes\n")
        
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            print("\n⚠️  Cerrando navegador...")
        
        browser.close()
        print("✅ Navegador cerrado")
        
        print("\n" + "=" * 80)
        print("  ✅ VERIFICACIÓN COMPLETADA")
        print("=" * 80)
        print("\n📸 Revisa: dashboard_screenshot.png")
        print("🔗 URL del dashboard: " + BASE_URL + "/gestion/\n")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
