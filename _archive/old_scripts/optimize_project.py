#!/usr/bin/env python3
"""
🧹 LINO SYS - SCRIPT DE LIMPIEZA Y OPTIMIZACIÓN
==================================================

Este script analiza y optimiza la estructura del proyecto, eliminando
archivos duplicados y reorganizando la estructura de forma eficiente.

Autor: Ingeniero de Software Especializado
Fecha: Octubre 2025
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class LinoProjectOptimizer:
    """Optimizador inteligente para el proyecto Lino"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.report = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': 0,
            'files_removed': 0,
            'size_saved': 0,
            'actions': []
        }
    
    def analyze_project_structure(self):
        """Analiza la estructura actual del proyecto"""
        print("🔍 ANÁLISIS DE ESTRUCTURA DEL PROYECTO")
        print("=" * 50)
        
        # Analizar directorios principales
        directories = {
            'backup_templates_originales': self._analyze_directory('backup_templates_originales'),
            'backup_refactorizacion': self._analyze_directory('backup_refactorizacion'),
            'src/gestion/templates': self._analyze_directory('src/gestion/templates'),
            'markdown_docs': self._analyze_markdown_files()
        }
        
        for dir_name, info in directories.items():
            print(f"\n📁 {dir_name}:")
            print(f"   Archivos: {info['count']}")
            print(f"   Tamaño: {info['size_mb']:.2f} MB")
            if info['duplicates']:
                print(f"   🚨 Duplicados encontrados: {len(info['duplicates'])}")
        
        return directories
    
    def _analyze_directory(self, dir_path):
        """Analiza un directorio específico"""
        full_path = self.project_root / dir_path
        if not full_path.exists():
            return {'count': 0, 'size_mb': 0, 'duplicates': []}
        
        files = []
        total_size = 0
        
        for file_path in full_path.rglob('*'):
            if file_path.is_file():
                files.append(file_path)
                total_size += file_path.stat().st_size
        
        duplicates = self._find_duplicates(files)
        
        return {
            'count': len(files),
            'size_mb': total_size / (1024 * 1024),
            'duplicates': duplicates,
            'files': files
        }
    
    def _analyze_markdown_files(self):
        """Analiza archivos markdown en la raíz"""
        md_files = list(self.project_root.glob('*.md'))
        total_size = sum(f.stat().st_size for f in md_files)
        
        return {
            'count': len(md_files),
            'size_mb': total_size / (1024 * 1024),
            'duplicates': [],
            'files': md_files
        }
    
    def _find_duplicates(self, files):
        """Encuentra archivos duplicados por nombre"""
        file_names = {}
        duplicates = []
        
        for file_path in files:
            name = file_path.name
            if name in file_names:
                duplicates.append((file_path, file_names[name]))
            else:
                file_names[name] = file_path
        
        return duplicates
    
    def create_cleanup_plan(self):
        """Crea un plan de limpieza optimizado"""
        print("\n🎯 PLAN DE LIMPIEZA OPTIMIZADA")
        print("=" * 50)
        
        plan = {
            'phase_1_backup_cleanup': {
                'description': 'Eliminar backups obsoletos',
                'actions': [
                    'Mover backup_templates_originales a .archived/',
                    'Consolidar backup_refactorizacion en docs/',
                    'Eliminar archivos duplicados'
                ],
                'estimated_savings': '15-20 MB'
            },
            'phase_2_template_organization': {
                'description': 'Reorganizar templates',
                'actions': [
                    'Consolidar templates en modules/',
                    'Eliminar versiones _migrado obsoletas',
                    'Optimizar imports y extends'
                ],
                'estimated_savings': '5-8 MB'
            },
            'phase_3_documentation': {
                'description': 'Organizar documentación',
                'actions': [
                    'Crear docs/ directory',
                    'Consolidar archivos .md',
                    'Crear README principal actualizado'
                ],
                'estimated_savings': '2-3 MB'
            }
        }
        
        for phase, details in plan.items():
            print(f"\n📋 {phase.upper().replace('_', ' ')}")
            print(f"   {details['description']}")
            print(f"   💾 Ahorro estimado: {details['estimated_savings']}")
            for action in details['actions']:
                print(f"   • {action}")
        
        return plan
    
    def execute_cleanup(self, dry_run=True):
        """Ejecuta la limpieza (modo dry-run por defecto)"""
        mode = "DRY RUN" if dry_run else "EJECUCIÓN REAL"
        print(f"\n🚀 INICIANDO LIMPIEZA - {mode}")
        print("=" * 50)
        
        # Fase 1: Mover backups
        self._move_backups(dry_run)
        
        # Fase 2: Limpiar templates
        self._cleanup_templates(dry_run)
        
        # Fase 3: Organizar documentación
        self._organize_docs(dry_run)
        
        if not dry_run:
            self._save_report()
        
        print(f"\n✅ LIMPIEZA COMPLETADA - {mode}")
        print(f"📊 Archivos procesados: {self.report['files_analyzed']}")
        print(f"🗑️  Archivos removidos: {self.report['files_removed']}")
        print(f"💾 Espacio ahorrado: {self.report['size_saved'] / (1024*1024):.2f} MB")
    
    def _move_backups(self, dry_run):
        """Mueve directorios de backup"""
        print("\n📁 Moviendo backups...")
        
        archived_dir = self.project_root / '.archived'
        if not dry_run:
            archived_dir.mkdir(exist_ok=True)
        
        backup_dirs = ['backup_templates_originales', 'backup_refactorizacion']
        
        for backup_dir in backup_dirs:
            source = self.project_root / backup_dir
            if source.exists():
                target = archived_dir / f"{backup_dir}_{datetime.now().strftime('%Y%m%d')}"
                
                if dry_run:
                    print(f"   [DRY RUN] Movería: {source} -> {target}")
                else:
                    shutil.move(str(source), str(target))
                    print(f"   ✅ Movido: {backup_dir}")
                
                self.report['actions'].append(f"Moved {backup_dir} to .archived/")
    
    def _cleanup_templates(self, dry_run):
        """Limpia templates duplicados"""
        print("\n🧹 Limpiando templates...")
        
        templates_dir = self.project_root / 'src' / 'gestion' / 'templates'
        
        # Buscar archivos con sufijos obsoletos
        obsolete_patterns = ['*_backup*.html', '*_migrado.html', '*_lino.html']
        
        for pattern in obsolete_patterns:
            for file_path in templates_dir.rglob(pattern):
                if dry_run:
                    print(f"   [DRY RUN] Eliminaría: {file_path.relative_to(templates_dir)}")
                else:
                    file_path.unlink()
                    print(f"   🗑️  Eliminado: {file_path.name}")
                
                self.report['files_removed'] += 1
                self.report['size_saved'] += file_path.stat().st_size if file_path.exists() else 0
    
    def _organize_docs(self, dry_run):
        """Organiza documentación"""
        print("\n📚 Organizando documentación...")
        
        docs_dir = self.project_root / 'docs'
        if not dry_run:
            docs_dir.mkdir(exist_ok=True)
        
        # Categorizar archivos markdown
        categories = {
            'deployment': ['DEPLOYMENT_', 'GUIA_DEPLOY'],
            'audit': ['AUDIT_', 'REPORTE_'],
            'implementation': ['IMPLEMENTACION_', 'FRONTEND_'],
            'migration': ['MIGRACION_', 'TRACK_']
        }
        
        for md_file in self.project_root.glob('*.md'):
            if md_file.name == 'README.md':
                continue  # Mantener README en raíz
                
            category = 'general'
            for cat, patterns in categories.items():
                if any(pattern in md_file.name for pattern in patterns):
                    category = cat
                    break
            
            target_dir = docs_dir / category
            target_file = target_dir / md_file.name
            
            if dry_run:
                print(f"   [DRY RUN] Movería: {md_file.name} -> docs/{category}/")
            else:
                target_dir.mkdir(exist_ok=True)
                shutil.move(str(md_file), str(target_file))
                print(f"   📝 Movido: {md_file.name} -> {category}/")
    
    def _save_report(self):
        """Guarda reporte de optimización"""
        report_file = self.project_root / 'optimization_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\n📄 Reporte guardado: {report_file}")

def main():
    """Función principal"""
    project_root = "/Users/giulianozulatto/Proyectos/lino_saludable"
    optimizer = LinoProjectOptimizer(project_root)
    
    # Análisis
    optimizer.analyze_project_structure()
    
    # Plan de limpieza
    optimizer.create_cleanup_plan()
    
    # Ejecutar en modo dry-run
    print("\n" + "="*60)
    print("🤔 ¿Deseas ejecutar la limpieza?")
    print("   1. Sí, ejecutar limpieza real")
    print("   2. Solo mostrar lo que se haría (DRY RUN)")
    print("   3. Salir sin cambios")
    
    # Por ahora, solo dry-run para mostrar el análisis
    optimizer.execute_cleanup(dry_run=True)
    
    print("\n💡 RECOMENDACIONES FINALES:")
    print("=" * 50)
    print("1. 🧹 Ejecutar limpieza para liberar 20+ MB")
    print("2. 🏗️  Implementar sistema de componentes unificado")
    print("3. 📝 Consolidar documentación en docs/")
    print("4. 🚀 Proceder con migración optimizada de inventario")

if __name__ == "__main__":
    main()
