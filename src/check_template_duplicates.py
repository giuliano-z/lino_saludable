import os
from collections import defaultdict

# Función para encontrar archivos .html
def find_html_files(directory):
    html_files = []
    
    for root, dirs, files in os.walk(directory):
        # Omitir directorios de backup
        dirs[:] = [d for d in dirs if not d.startswith('_') and 'backup' not in d.lower()]
        
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                # Obtener ruta relativa desde templates
                if 'templates' in full_path:
                    rel_path = full_path.split('templates/')[-1]
                    html_files.append((rel_path, full_path))
    
    return html_files

print("=== VERIFICACIÓN DE PLANTILLAS DUPLICADAS ===\n")

# Buscar en el directorio de templates
templates_dir = 'gestion/templates'
html_files = find_html_files(templates_dir)

# Agrupar por nombre de archivo
files_by_name = defaultdict(list)
for rel_path, full_path in html_files:
    filename = os.path.basename(rel_path)
    files_by_name[filename].append((rel_path, full_path))

print("Archivos duplicados por nombre:")
duplicates_found = False
for filename, paths in files_by_name.items():
    if len(paths) > 1:
        duplicates_found = True
        print(f"\n📄 {filename} ({len(paths)} copias):")
        for rel_path, full_path in paths:
            size = os.path.getsize(full_path)
            print(f"  - {rel_path} ({size} bytes)")

if not duplicates_found:
    print("  ✅ No hay nombres de archivos duplicados")

print(f"\nTotal de plantillas encontradas: {len(html_files)}")

# Verificar estructura
print("\n=== ESTRUCTURA DE PLANTILLAS ===")
structure = defaultdict(list)
for rel_path, full_path in html_files:
    parts = rel_path.split('/')
    if len(parts) > 1:
        main_dir = parts[0]
        structure[main_dir].append(rel_path)

for main_dir, files in sorted(structure.items()):
    print(f"\n📁 {main_dir}/ ({len(files)} archivos)")
    for file in sorted(files)[:5]:  # Mostrar solo los primeros 5
        print(f"  - {file}")
    if len(files) > 5:
        print(f"  ... y {len(files) - 5} más")
