import os

def remove_empty_files(directory):
    removed_files = []
    
    for root, dirs, files in os.walk(directory):
        # Omitir directorios de backup
        dirs[:] = [d for d in dirs if not d.startswith('_') and 'backup' not in d.lower()]
        
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                try:
                    # Verificar si el archivo está vacío
                    if os.path.getsize(full_path) == 0:
                        os.remove(full_path)
                        removed_files.append(full_path)
                        print(f"🗑️  Eliminado: {full_path}")
                except OSError as e:
                    print(f"❌ Error al eliminar {full_path}: {e}")
    
    return removed_files

print("=== LIMPIEZA DE ARCHIVOS VACÍOS ===\n")

# Limpiar en el directorio de templates
templates_dir = 'gestion/templates'
removed = remove_empty_files(templates_dir)

print(f"\n✅ Se eliminaron {len(removed)} archivos vacíos")

if removed:
    print("\nArchivos eliminados:")
    for file in removed:
        print(f"  - {file}")
else:
    print("No se encontraron archivos vacíos para eliminar")
