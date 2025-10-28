#!/usr/bin/env python3
"""
🔍 AUDIT MANUAL INTERACTIVO - LINO SALUDABLE
Sistema de testing manual asistido por IA para verificar funcionalidad y diseño
"""
import webbrowser
import time
import os
from datetime import datetime

class LinoAuditInteractivo:
    """Clase para realizar audit manual sistemático"""
    
    def __init__(self):
        self.BASE_URL = "http://127.0.0.1:8000"
        self.resultados = []
        self.modulos_auditados = []
        
        # Colores para terminal
        self.GREEN = '\033[92m'
        self.RED = '\033[91m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.PURPLE = '\033[95m'
        self.CYAN = '\033[96m'
        self.END = '\033[0m'
        self.BOLD = '\033[1m'
    
    def mostrar_header(self):
        """Muestra el header del audit"""
        print(f"""
{self.CYAN}╔══════════════════════════════════════════════════════════════════════════╗
║  🚀 AUDIT MANUAL INTERACTIVO - LINO SALUDABLE                           ║  
║  📅 {datetime.now().strftime('%d de %B %Y - %H:%M')}                                        ║
║  🎯 Testing Sistemático Pre-Producción                                  ║
╚══════════════════════════════════════════════════════════════════════════╝{self.END}

{self.BOLD}{self.BLUE}🔍 INICIANDO AUDIT MANUAL PROFESIONAL{self.END}
""")
    
    def esperar_confirmacion(self, mensaje="¿Continuar?"):
        """Espera confirmación del usuario"""
        respuesta = input(f"\n{self.YELLOW}⏸️  {mensaje} (Enter para continuar, 'q' para salir): {self.END}")
        if respuesta.lower() == 'q':
            self.finalizar_audit()
            exit(0)
        return True
    
    def registrar_resultado(self, modulo, test, resultado, observaciones=""):
        """Registra resultado de un test"""
        self.resultados.append({
            'timestamp': datetime.now(),
            'modulo': modulo,
            'test': test,
            'resultado': resultado,
            'observaciones': observaciones
        })
        
        icon = "✅" if resultado == "OK" else "❌" if resultado == "ERROR" else "⚠️"
        color = self.GREEN if resultado == "OK" else self.RED if resultado == "ERROR" else self.YELLOW
        
        print(f"{color}{icon} {modulo} - {test}{self.END}")
        if observaciones:
            print(f"   📝 {observaciones}")
    
    def abrir_url(self, ruta, descripcion):
        """Abre una URL en el navegador"""
        url = f"{self.BASE_URL}{ruta}"
        print(f"\n{self.CYAN}🌐 Abriendo: {descripcion}{self.END}")
        print(f"   📍 URL: {url}")
        webbrowser.open(url)
        time.sleep(2)  # Dar tiempo para que se abra
    
    def audit_panel_control(self):
        """Audit del Panel de Control / Dashboard"""
        print(f"\n{self.BOLD}{self.PURPLE}📊 MÓDULO 1: PANEL DE CONTROL{self.END}")
        print("="*60)
        
        self.abrir_url("", "Panel de Control Principal")
        
        print(f"\n{self.YELLOW}🔍 VERIFICAR:{self.END}")
        print("1. ¿La página carga correctamente?")
        print("2. ¿Se muestran las estadísticas principales?")
        print("3. ¿Los números reflejan los datos reales (69 productos)?")
        print("4. ¿El diseño es responsive en diferentes tamaños?")
        print("5. ¿Los colores y tipografía son consistentes?")
        print("6. ¿Los links de navegación funcionan?")
        
        self.esperar_confirmacion("¿Panel de Control funciona correctamente?")
        
        # Registrar resultados basados en observación manual
        resultado = input(f"{self.CYAN}Resultado (OK/ADVERTENCIA/ERROR): {self.END}").upper()
        observaciones = input(f"{self.CYAN}Observaciones (opcional): {self.END}")
        
        self.registrar_resultado("Panel Control", "Funcionalidad General", 
                                resultado or "OK", observaciones)
        
        self.modulos_auditados.append("Panel Control")
    
    def audit_productos(self):
        """Audit del módulo de Productos"""
        print(f"\n{self.BOLD}{self.PURPLE}🛍️ MÓDULO 2: PRODUCTOS{self.END}")
        print("="*60)
        
        # Test 1: Lista de productos
        self.abrir_url("/gestion/productos/", "Lista de Productos")
        
        print(f"\n{self.YELLOW}🔍 VERIFICAR LISTA DE PRODUCTOS:{self.END}")
        print("1. ¿Se muestran los 69 productos correctamente?")
        print("2. ¿Los precios y stocks son correctos?")
        print("3. ¿La tabla es responsive?")
        print("4. ¿Los filtros/búsquedas funcionan?")
        print("5. ¿Los botones de acción están visibles?")
        
        self.esperar_confirmacion("¿Lista de productos OK?")
        
        resultado = input(f"{self.CYAN}Resultado Lista (OK/ADVERTENCIA/ERROR): {self.END}").upper()
        observaciones = input(f"{self.CYAN}Observaciones: {self.END}")
        
        self.registrar_resultado("Productos", "Lista de Productos", 
                                resultado or "OK", observaciones)
        
        # Test 2: Crear producto (sabemos que puede fallar)
        print(f"\n{self.YELLOW}⚠️ TESTING CREAR PRODUCTO (puede fallar por template):{self.END}")
        self.abrir_url("/gestion/productos/crear/", "Crear Producto")
        
        time.sleep(3)
        resultado_crear = input(f"{self.CYAN}¿Formulario crear carga? (OK/ERROR): {self.END}").upper()
        
        if resultado_crear == "ERROR":
            print(f"{self.YELLOW}📝 Esto era esperado - template en desarrollo{self.END}")
            observaciones_crear = "Template necesita corrección (esperado)"
        else:
            observaciones_crear = input(f"{self.CYAN}Observaciones formulario: {self.END}")
        
        self.registrar_resultado("Productos", "Crear Producto", 
                                resultado_crear or "ERROR", observaciones_crear)
        
        self.modulos_auditados.append("Productos")
    
    def audit_ventas(self):
        """Audit del módulo de Ventas"""
        print(f"\n{self.BOLD}{self.PURPLE}💰 MÓDULO 3: VENTAS{self.END}")
        print("="*60)
        
        # Test 1: Lista de ventas
        self.abrir_url("/gestion/ventas/", "Lista de Ventas")
        
        print(f"\n{self.YELLOW}🔍 VERIFICAR LISTA DE VENTAS:{self.END}")
        print("1. ¿Se muestran las ventas históricas correctamente?")
        print("2. ¿Los totales se calculan bien?")
        print("3. ¿Las fechas son correctas?")
        print("4. ¿Se pueden ver detalles de cada venta?")
        
        self.esperar_confirmacion("¿Lista de ventas OK?")
        
        resultado = input(f"{self.CYAN}Resultado Lista Ventas (OK/ADVERTENCIA/ERROR): {self.END}").upper()
        observaciones = input(f"{self.CYAN}Observaciones: {self.END}")
        
        self.registrar_resultado("Ventas", "Lista de Ventas", 
                                resultado or "OK", observaciones)
        
        # Test 2: Crear venta (puede fallar)
        print(f"\n{self.YELLOW}⚠️ TESTING CREAR VENTA (puede fallar por template):{self.END}")
        self.abrir_url("/gestion/ventas/crear/", "Crear Venta")
        
        time.sleep(3)
        resultado_crear = input(f"{self.CYAN}¿Formulario crear venta carga? (OK/ERROR): {self.END}").upper()
        observaciones_crear = input(f"{self.CYAN}Observaciones: {self.END}")
        
        self.registrar_resultado("Ventas", "Crear Venta", 
                                resultado_crear or "ERROR", observaciones_crear)
        
        self.modulos_auditados.append("Ventas")
    
    def audit_compras(self):
        """Audit del módulo de Compras"""
        print(f"\n{self.BOLD}{self.PURPLE}📦 MÓDULO 4: COMPRAS{self.END}")
        print("="*60)
        
        # Lista de compras
        self.abrir_url("/gestion/compras/", "Lista de Compras")
        
        print(f"\n{self.YELLOW}🔍 VERIFICAR COMPRAS:{self.END}")
        print("1. ¿Se muestran las compras correctamente?")
        print("2. ¿Los datos de materias primas son correctos?")
        print("3. ¿Los cálculos de costos son precisos?")
        
        self.esperar_confirmacion("¿Módulo compras funciona?")
        
        resultado = input(f"{self.CYAN}Resultado Compras (OK/ADVERTENCIA/ERROR): {self.END}").upper()
        observaciones = input(f"{self.CYAN}Observaciones: {self.END}")
        
        self.registrar_resultado("Compras", "Funcionalidad General", 
                                resultado or "OK", observaciones)
        
        self.modulos_auditados.append("Compras")
    
    def audit_navegacion_general(self):
        """Audit de navegación general"""
        print(f"\n{self.BOLD}{self.PURPLE}🧭 NAVEGACIÓN GENERAL{self.END}")
        print("="*60)
        
        print(f"\n{self.YELLOW}🔍 VERIFICAR NAVEGACIÓN:{self.END}")
        print("1. ¿El menú principal es intuitivo?")
        print("2. ¿Los breadcrumbs funcionan?")
        print("3. ¿Los links internos están operativos?")
        print("4. ¿El diseño es consistente entre páginas?")
        print("5. ¿La experiencia mobile es aceptable?")
        
        self.esperar_confirmacion("¿Navegación general OK?")
        
        resultado = input(f"{self.CYAN}Resultado Navegación (OK/ADVERTENCIA/ERROR): {self.END}").upper()
        observaciones = input(f"{self.CYAN}Observaciones: {self.END}")
        
        self.registrar_resultado("General", "Navegación", 
                                resultado or "OK", observaciones)
    
    def generar_reporte_final(self):
        """Genera el reporte final del audit"""
        print(f"\n{self.BOLD}{self.CYAN}📋 GENERANDO REPORTE FINAL{self.END}")
        
        total_tests = len(self.resultados)
        exitosos = len([r for r in self.resultados if r['resultado'] == 'OK'])
        advertencias = len([r for r in self.resultados if r['resultado'] == 'ADVERTENCIA'])
        errores = len([r for r in self.resultados if r['resultado'] == 'ERROR'])
        
        tasa_exito = (exitosos / total_tests * 100) if total_tests > 0 else 0
        
        reporte = f"""
# 📊 REPORTE AUDIT MANUAL - LINO SALUDABLE

**Fecha:** {datetime.now().strftime('%d de %B %Y - %H:%M')}
**Auditor:** Testing Manual Interactivo
**Módulos Auditados:** {len(self.modulos_auditados)}

## 🎯 RESUMEN EJECUTIVO

**Tasa de Éxito: {tasa_exito:.1f}% ({exitosos}/{total_tests} tests exitosos)**

- ✅ **Tests Exitosos:** {exitosos}
- ⚠️ **Advertencias:** {advertencias} 
- ❌ **Errores:** {errores}

## 📝 RESULTADOS DETALLADOS

"""
        
        for resultado in self.resultados:
            icon = "✅" if resultado['resultado'] == "OK" else "❌" if resultado['resultado'] == "ERROR" else "⚠️"
            reporte += f"""
### {icon} {resultado['modulo']} - {resultado['test']}
- **Resultado:** {resultado['resultado']}
- **Timestamp:** {resultado['timestamp'].strftime('%H:%M:%S')}
"""
            if resultado['observaciones']:
                reporte += f"- **Observaciones:** {resultado['observaciones']}\n"
        
        reporte += f"""

## 🎯 CONCLUSIONES

**Módulos Auditados:** {', '.join(self.modulos_auditados)}

**Sistema {"APROBADO" if tasa_exito >= 70 else "REQUIERE CORRECCIONES"} para producción**

---
*Generado por Sistema de Audit Manual Interactivo*
"""
        
        # Guardar reporte
        with open('REPORTE_AUDIT_MANUAL.md', 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print(f"\n{self.GREEN}✅ Reporte guardado en: REPORTE_AUDIT_MANUAL.md{self.END}")
        
        return reporte
    
    def finalizar_audit(self):
        """Finaliza el audit y muestra resumen"""
        print(f"\n{self.BOLD}{self.CYAN}🎉 AUDIT MANUAL COMPLETADO{self.END}")
        
        if self.resultados:
            reporte = self.generar_reporte_final()
            print(f"\n{self.BLUE}📊 Resumen Final:{self.END}")
            print(f"- Módulos auditados: {len(self.modulos_auditados)}")
            print(f"- Tests realizados: {len(self.resultados)}")
            print(f"- Tiempo total: Interactivo")
        
        print(f"\n{self.BOLD}{self.GREEN}🚀 ¡EXCELENTE TRABAJO! LINO SALUDABLE AUDITADO PROFESIONALMENTE{self.END}")
    
    def ejecutar_audit_completo(self):
        """Ejecuta el audit completo"""
        self.mostrar_header()
        
        print(f"{self.BOLD}🎯 PLAN DE AUDIT SISTEMÁTICO:{self.END}")
        print("1. Panel de Control")
        print("2. Módulo Productos") 
        print("3. Módulo Ventas")
        print("4. Módulo Compras")
        print("5. Navegación General")
        
        self.esperar_confirmacion("¿Iniciar audit completo?")
        
        try:
            # Ejecutar audits por módulo
            self.audit_panel_control()
            self.audit_productos()
            self.audit_ventas()
            self.audit_compras() 
            self.audit_navegacion_general()
            
            # Finalizar
            self.finalizar_audit()
            
        except KeyboardInterrupt:
            print(f"\n{self.YELLOW}⚠️ Audit interrumpido por usuario{self.END}")
            self.finalizar_audit()
        except Exception as e:
            print(f"\n{self.RED}❌ Error en audit: {str(e)}{self.END}")
            self.finalizar_audit()

def main():
    """Función principal"""
    auditor = LinoAuditInteractivo()
    auditor.ejecutar_audit_completo()

if __name__ == '__main__':
    main()
