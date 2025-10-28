#!/usr/bin/env python3
"""
LINO DESIGN SYSTEM V3 - VERIFICADOR COMPLETO
Script avanzado de verificación del sistema de diseño
Enfoque: Ingeniería senior con métricas detalladas
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class LinoSystemVerifier:
    """Verificador avanzado del sistema de diseño LINO V3"""
    
    def __init__(self):
        self.base_path = Path("/Users/giulianozulatto/Proyectos/lino_saludable")
        self.src_path = self.base_path / "src"
        self.css_path = self.src_path / "static" / "css"
        self.templates_path = self.src_path / "gestion" / "templates" / "gestion"
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "system_version": "3.0",
            "components": {},
            "metrics": {},
            "recommendations": []
        }
    
    def verify_css_files(self):
        """Verifica la existencia y tamaño de archivos CSS"""
        print("🔍 VERIFICANDO ARCHIVOS CSS DEL SISTEMA")
        print("=" * 50)
        
        css_files = {
            "lino-design-system.css": {"min_size": 15000, "description": "Sistema base"},
            "lino-kpi-cards.css": {"min_size": 8000, "description": "Componentes KPI"},
            "lino-forms.css": {"min_size": 10000, "description": "Sistema de formularios"},
            "lino-tables.css": {"min_size": 10000, "description": "Sistema de tablas"}
        }
        
        css_results = {}
        total_size = 0
        
        for filename, config in css_files.items():
            file_path = self.css_path / filename
            if file_path.exists():
                size = file_path.stat().st_size
                total_size += size
                status = "✅" if size >= config["min_size"] else "⚠️ "
                print(f"{status} {filename}: {size:,} bytes - {config['description']}")
                
                css_results[filename] = {
                    "exists": True,
                    "size": size,
                    "status": "ok" if size >= config["min_size"] else "warning",
                    "description": config["description"]
                }
            else:
                print(f"❌ {filename}: NO ENCONTRADO - {config['description']}")
                css_results[filename] = {
                    "exists": False,
                    "size": 0,
                    "status": "error",
                    "description": config["description"]
                }
        
        self.results["components"]["css_files"] = css_results
        self.results["metrics"]["total_css_size"] = total_size
        print(f"\n📊 Tamaño total del sistema: {total_size:,} bytes ({total_size/1024:.1f} KB)")
        print()
    
    def verify_css_variables(self):
        """Verifica las variables CSS definidas"""
        print("🎨 VERIFICANDO VARIABLES CSS")
        print("=" * 50)
        
        system_file = self.css_path / "lino-design-system.css"
        if not system_file.exists():
            print("❌ Archivo base no encontrado")
            return
        
        content = system_file.read_text()
        
        critical_variables = {
            # Colores
            "--lino-primary": "Color principal",
            "--lino-olive": "Verde oliva marca", 
            "--lino-orange": "Naranja energético",
            "--lino-success": "Verde éxito",
            "--lino-danger": "Rojo peligro",
            "--lino-warning": "Amarillo advertencia",
            "--lino-info": "Azul información",
            
            # Espaciado
            "--lino-spacing-xs": "Espaciado XS",
            "--lino-spacing-sm": "Espaciado SM", 
            "--lino-spacing-md": "Espaciado MD",
            "--lino-spacing-lg": "Espaciado LG",
            "--lino-spacing-xl": "Espaciado XL",
            
            # Tipografía
            "--lino-font-family-primary": "Fuente principal",
            "--lino-text-xs": "Texto XS",
            "--lino-text-sm": "Texto SM",
            "--lino-text-base": "Texto base",
            "--lino-text-lg": "Texto LG",
            
            # Diseño
            "--lino-border-radius-base": "Radio base",
            "--lino-border-radius-lg": "Radio grande",
            "--lino-transition-base": "Transición base",
            "--lino-shadow-sm": "Sombra pequeña",
            "--lino-shadow-lg": "Sombra grande"
        }
        
        variables_found = {}
        missing_variables = []
        
        for variable, description in critical_variables.items():
            if variable in content:
                print(f"✅ {variable}: {description}")
                variables_found[variable] = description
            else:
                print(f"❌ {variable}: {description} - NO DEFINIDA")
                missing_variables.append(variable)
        
        self.results["components"]["css_variables"] = {
            "found": variables_found,
            "missing": missing_variables,
            "total_found": len(variables_found),
            "total_expected": len(critical_variables),
            "coverage_percentage": round((len(variables_found) / len(critical_variables)) * 100, 1)
        }
        
        print(f"\n📊 Cobertura de variables: {len(variables_found)}/{len(critical_variables)} ({self.results['components']['css_variables']['coverage_percentage']}%)")
        print()
    
    def verify_template_integration(self):
        """Verifica la integración en templates"""
        print("📄 VERIFICANDO INTEGRACIÓN EN TEMPLATES")
        print("=" * 50)
        
        templates_to_check = {
            "dashboard.html": "Dashboard principal",
            "dashboard_rentabilidad.html": "Dashboard rentabilidad",
            "base.html": "Template base"
        }
        
        components_to_find = {
            "lino-kpi-card": "KPI Cards",
            "lino-card": "Cards generales",
            "lino-alert": "Sistema de alertas", 
            "lino-action-btn": "Botones de acción",
            "lino-btn": "Botones del sistema",
            "lino-form": "Formularios",
            "lino-table": "Tablas"
        }
        
        template_results = {}
        
        for template_name, template_desc in templates_to_check.items():
            template_path = self.templates_path / template_name
            
            if not template_path.exists():
                print(f"❌ {template_name}: NO ENCONTRADO")
                template_results[template_name] = {"exists": False}
                continue
            
            content = template_path.read_text()
            print(f"\n📄 {template_name} ({template_desc}):")
            
            template_components = {}
            for component, component_desc in components_to_find.items():
                count = len(re.findall(component, content))
                if count > 0:
                    print(f"  ✅ {component}: {count} uso(s) - {component_desc}")
                    template_components[component] = count
                else:
                    print(f"  ⚠️  {component}: NO USADO - {component_desc}")
                    template_components[component] = 0
            
            template_results[template_name] = {
                "exists": True,
                "components": template_components,
                "total_components": sum(template_components.values())
            }
        
        self.results["components"]["templates"] = template_results
        print()
    
    def verify_css_inclusion(self):
        """Verifica que los CSS estén incluidos en base.html"""
        print("🔗 VERIFICANDO INCLUSIÓN DE CSS EN BASE.HTML")
        print("=" * 50)
        
        base_template = self.templates_path / "base.html"
        if not base_template.exists():
            print("❌ base.html no encontrado")
            return
        
        content = base_template.read_text()
        
        css_inclusions = {
            "lino-design-system.css": "Sistema base",
            "lino-kpi-cards.css": "Componentes KPI",
            "lino-forms.css": "Formularios", 
            "lino-tables.css": "Tablas"
        }
        
        inclusion_results = {}
        
        for css_file, description in css_inclusions.items():
            if css_file in content:
                print(f"✅ {css_file}: INCLUIDO - {description}")
                inclusion_results[css_file] = True
            else:
                print(f"❌ {css_file}: NO INCLUIDO - {description}")
                inclusion_results[css_file] = False
        
        self.results["components"]["css_inclusion"] = inclusion_results
        print()
    
    def calculate_metrics(self):
        """Calcula métricas del sistema"""
        print("📊 CALCULANDO MÉTRICAS DEL SISTEMA")
        print("=" * 50)
        
        # Métricas de archivos CSS
        css_files = self.results["components"]["css_files"]
        css_ok = sum(1 for f in css_files.values() if f["status"] == "ok")
        css_total = len(css_files)
        
        # Métricas de variables
        variables = self.results["components"]["css_variables"]
        var_coverage = variables["coverage_percentage"]
        
        # Métricas de templates
        templates = self.results["components"]["templates"]
        templates_with_components = sum(1 for t in templates.values() 
                                      if t.get("exists", False) and t.get("total_components", 0) > 0)
        templates_total = len([t for t in templates.values() if t.get("exists", False)])
        
        # Métricas de inclusión CSS
        inclusions = self.results["components"]["css_inclusion"]
        css_included = sum(1 for included in inclusions.values() if included)
        css_inclusion_total = len(inclusions)
        
        metrics = {
            "css_files_health": round((css_ok / css_total) * 100, 1),
            "variables_coverage": var_coverage,
            "templates_integration": round((templates_with_components / templates_total) * 100, 1) if templates_total > 0 else 0,
            "css_inclusion_rate": round((css_included / css_inclusion_total) * 100, 1),
        }
        
        # Puntuación general
        scores = [
            metrics["css_files_health"],
            metrics["variables_coverage"], 
            metrics["templates_integration"],
            metrics["css_inclusion_rate"]
        ]
        overall_score = round(sum(scores) / len(scores), 1)
        metrics["overall_score"] = overall_score
        
        self.results["metrics"].update(metrics)
        
        print(f"📁 Salud archivos CSS: {metrics['css_files_health']}%")
        print(f"🎨 Cobertura variables: {metrics['variables_coverage']}%") 
        print(f"📄 Integración templates: {metrics['templates_integration']}%")
        print(f"🔗 Inclusión CSS: {metrics['css_inclusion_rate']}%")
        print(f"🎯 PUNTUACIÓN GENERAL: {overall_score}%")
        print()
        
        return overall_score
    
    def generate_recommendations(self):
        """Genera recomendaciones basadas en el análisis"""
        print("💡 GENERANDO RECOMENDACIONES")
        print("=" * 50)
        
        recommendations = []
        
        # Recomendaciones basadas en métricas
        metrics = self.results["metrics"]
        
        if metrics["css_files_health"] < 100:
            recommendations.append({
                "type": "critical",
                "title": "Archivos CSS incompletos",
                "description": "Algunos archivos CSS no cumplen el tamaño mínimo esperado",
                "action": "Verificar que todos los componentes estén implementados completamente"
            })
        
        if metrics["variables_coverage"] < 90:
            recommendations.append({
                "type": "high", 
                "title": "Variables CSS faltantes",
                "description": f"Cobertura de variables: {metrics['variables_coverage']}%",
                "action": "Definir las variables CSS faltantes en lino-design-system.css"
            })
        
        if metrics["templates_integration"] < 80:
            recommendations.append({
                "type": "medium",
                "title": "Integración de templates incompleta", 
                "description": "Algunos templates no están usando los nuevos componentes",
                "action": "Migrar templates restantes al sistema de componentes V3"
            })
        
        if metrics["css_inclusion_rate"] < 100:
            recommendations.append({
                "type": "critical",
                "title": "CSS no incluidos en base.html",
                "description": "Algunos archivos CSS no están siendo cargados",
                "action": "Agregar los <link> faltantes en el template base"
            })
        
        # Recomendaciones de próximos pasos
        if metrics["overall_score"] >= 80:
            recommendations.append({
                "type": "success",
                "title": "Sistema bien implementado",
                "description": "El sistema de diseño está funcionando correctamente",
                "action": "Continuar con la migración de templates restantes y optimizaciones"
            })
        
        if metrics["overall_score"] >= 90:
            recommendations.append({
                "type": "enhancement",
                "title": "Listo para optimizaciones",
                "description": "El sistema está maduro para mejoras avanzadas",
                "action": "Implementar tree-shaking CSS, dark mode, y componentes avanzados"
            })
        
        self.results["recommendations"] = recommendations
        
        for rec in recommendations:
            icon = {
                "critical": "🚨",
                "high": "⚠️ ",
                "medium": "📝",
                "success": "✅",
                "enhancement": "🚀"
            }.get(rec["type"], "💡")
            
            print(f"{icon} {rec['title']}")
            print(f"   {rec['description']}")
            print(f"   Acción: {rec['action']}")
            print()
    
    def generate_report(self):
        """Genera un reporte final del sistema"""
        print("📋 REPORTE FINAL DEL SISTEMA")
        print("=" * 50)
        
        overall_score = self.results["metrics"]["overall_score"]
        
        # Determinar estado del sistema
        if overall_score >= 90:
            status = "🟢 EXCELENTE"
            status_desc = "Sistema completamente funcional y optimizado"
        elif overall_score >= 80:
            status = "🟡 BUENO"  
            status_desc = "Sistema funcional con mejoras menores pendientes"
        elif overall_score >= 70:
            status = "🟠 REGULAR"
            status_desc = "Sistema parcialmente implementado"
        else:
            status = "🔴 CRÍTICO"
            status_desc = "Sistema requiere atención inmediata"
        
        print(f"Estado del Sistema: {status}")
        print(f"Descripción: {status_desc}")
        print(f"Puntuación General: {overall_score}%")
        print()
        
        print("📊 Resumen de Componentes:")
        print(f"• Archivos CSS: {len(self.results['components']['css_files'])} archivos")
        print(f"• Variables CSS: {self.results['components']['css_variables']['total_found']} definidas")
        print(f"• Templates integrados: {len([t for t in self.results['components']['templates'].values() if t.get('exists', False)])}")
        print(f"• Tamaño total: {self.results['metrics']['total_css_size']:,} bytes")
        print()
        
        print("🎯 Próximos pasos recomendados:")
        if overall_score >= 90:
            print("1. Implementar componentes avanzados (modales, tooltips)")
            print("2. Optimizar CSS con tree-shaking")
            print("3. Agregar dark mode completo") 
            print("4. Documentar patrones de uso")
        elif overall_score >= 80:
            print("1. Completar migración de templates restantes")
            print("2. Definir variables CSS faltantes")
            print("3. Optimizar componentes existentes")
        else:
            print("1. Revisar archivos CSS incompletos")
            print("2. Corregir inclusiones faltantes")
            print("3. Completar implementación base")
        
        print()
        
        # Guardar reporte JSON
        report_file = self.base_path / f"lino_system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Reporte detallado guardado en: {report_file.name}")
        print()
        
        return overall_score

def main():
    """Función principal"""
    print("🚀 LINO DESIGN SYSTEM V3 - VERIFICADOR AVANZADO")
    print("=" * 60)
    print("Análisis completo del sistema de diseño")
    print("Enfoque: Ingeniería senior + Métricas detalladas")
    print()
    
    verifier = LinoSystemVerifier()
    
    # Ejecutar verificaciones
    verifier.verify_css_files()
    verifier.verify_css_variables()
    verifier.verify_css_inclusion()
    verifier.verify_template_integration()
    
    # Calcular métricas y generar recomendaciones
    overall_score = verifier.calculate_metrics()
    verifier.generate_recommendations()
    final_score = verifier.generate_report()
    
    # Conclusión
    print("🎉 VERIFICACIÓN COMPLETADA")
    print(f"El LINO Design System V3 tiene una puntuación de {final_score}%")
    
    if final_score >= 90:
        print("¡Sistema excelente! Listo para producción y mejoras avanzadas. 🚀")
    elif final_score >= 80:
        print("Sistema sólido con implementación exitosa. Continuar con optimizaciones. ✅")
    else:
        print("Sistema requiere atención. Revisar recomendaciones. ⚠️")

if __name__ == "__main__":
    main()
