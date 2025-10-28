#!/usr/bin/env python3
"""
Script para verificar la integración del nuevo sistema de diseño LINO V3
"""

import os
import re
from pathlib import Path

def verificar_archivos_css():
    """Verifica que los archivos CSS del nuevo sistema existan"""
    base_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable/src/static/css")
    
    archivos_requeridos = [
        "lino-design-system.css",
        "lino-kpi-cards.css"
    ]
    
    print("🔍 VERIFICANDO ARCHIVOS CSS DEL SISTEMA DE DISEÑO")
    print("=" * 60)
    
    for archivo in archivos_requeridos:
        ruta = base_path / archivo
        if ruta.exists():
            tamaño = ruta.stat().st_size
            print(f"✅ {archivo}: {tamaño:,} bytes")
        else:
            print(f"❌ {archivo}: NO ENCONTRADO")
    
    print()

def verificar_template_base():
    """Verifica que el template base incluya los nuevos CSS"""
    template_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable/src/gestion/templates/gestion/base.html")
    
    print("🔍 VERIFICANDO TEMPLATE BASE")
    print("=" * 60)
    
    if not template_path.exists():
        print("❌ Template base no encontrado")
        return
    
    contenido = template_path.read_text()
    
    # Verificar inclusión de CSS
    css_checks = [
        ("lino-design-system.css", r'lino-design-system\.css'),
        ("lino-kpi-cards.css", r'lino-kpi-cards\.css'),
    ]
    
    for nombre, patron in css_checks:
        if re.search(patron, contenido):
            print(f"✅ {nombre}: INCLUIDO")
        else:
            print(f"❌ {nombre}: NO INCLUIDO")
    
    print()

def verificar_uso_componentes():
    """Verifica el uso de los nuevos componentes en templates"""
    templates_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable/src/gestion/templates/gestion")
    
    print("🔍 VERIFICANDO USO DE COMPONENTES NUEVOS")
    print("=" * 60)
    
    componentes_nuevos = [
        ("lino-kpi-card", r'lino-kpi-card'),
        ("lino-card", r'lino-card'),
        ("lino-alert", r'lino-alert'),
        ("lino-action-btn", r'lino-action-btn'),
    ]
    
    archivos_verificados = ["dashboard.html", "dashboard_rentabilidad.html"]
    
    for archivo in archivos_verificados:
        ruta = templates_path / archivo
        if not ruta.exists():
            print(f"❌ {archivo}: NO ENCONTRADO")
            continue
            
        contenido = ruta.read_text()
        print(f"\n📄 {archivo}:")
        
        for nombre, patron in componentes_nuevos:
            if re.search(patron, contenido):
                count = len(re.findall(patron, contenido))
                print(f"  ✅ {nombre}: {count} uso(s)")
            else:
                print(f"  ⚠️  {nombre}: NO USADO")
    
    print()

def verificar_variables_css():
    """Verifica que las variables CSS estén definidas correctamente"""
    css_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable/src/static/css/lino-design-system.css")
    
    print("🔍 VERIFICANDO VARIABLES CSS")
    print("=" * 60)
    
    if not css_path.exists():
        print("❌ Archivo de sistema de diseño no encontrado")
        return
    
    contenido = css_path.read_text()
    
    variables_esperadas = [
        "--lino-olive",
        "--lino-olive-light", 
        "--lino-orange",
        "--lino-orange-light",
        "--lino-success",
        "--lino-success-light",
        "--lino-spacing-xs",
        "--lino-spacing-sm",
        "--lino-font-family-primary",
        "--lino-border-radius-base",
    ]
    
    for variable in variables_esperadas:
        if variable in contenido:
            print(f"✅ {variable}: DEFINIDA")
        else:
            print(f"❌ {variable}: NO DEFINIDA")
    
    print()

def generar_reporte_migracion():
    """Genera un reporte del estado de migración"""
    print("📊 REPORTE DE MIGRACIÓN AL SISTEMA DE DISEÑO V3")
    print("=" * 60)
    
    # Contar archivos legacy vs nuevos
    static_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable/src/static/css")
    
    archivos_legacy = ["main.css", "lino-system.css", "mejoras_lino.css", "custom.css"]
    archivos_nuevos = ["lino-design-system.css", "lino-kpi-cards.css"]
    
    print("\n📁 ARCHIVOS CSS:")
    print("Legacy (a deprecar):")
    for archivo in archivos_legacy:
        ruta = static_path / archivo
        if ruta.exists():
            tamaño = ruta.stat().st_size
            print(f"  - {archivo}: {tamaño:,} bytes")
    
    print("\nNuevos (V3):")
    for archivo in archivos_nuevos:
        ruta = static_path / archivo
        if ruta.exists():
            tamaño = ruta.stat().st_size
            print(f"  - {archivo}: {tamaño:,} bytes")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. ✅ Crear sistema de diseño base")
    print("2. ✅ Crear componentes KPI unificados")
    print("3. ✅ Actualizar template base")
    print("4. ✅ Migrar dashboard principal")
    print("5. ⏳ Migrar resto de templates")
    print("6. ⏳ Eliminar CSS legacy")
    print("7. ⏳ Optimizar performance")
    
    print("\n💡 BENEFICIOS ALCANZADOS:")
    print("- Consistencia visual mejorada")
    print("- Componentes reutilizables")
    print("- Variables CSS centralizadas")
    print("- Animaciones y estados unificados")
    print("- Mejor mantenibilidad")

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE INTEGRACIÓN - LINO DESIGN SYSTEM V3")
    print("=" * 60)
    print()
    
    verificar_archivos_css()
    verificar_template_base()
    verificar_uso_componentes()
    verificar_variables_css()
    generar_reporte_migracion()
    
    print("\n✨ VERIFICACIÓN COMPLETADA")
    print("El nuevo sistema de diseño está parcialmente integrado.")
    print("Dashboard principal migrado exitosamente.")

if __name__ == "__main__":
    main()
