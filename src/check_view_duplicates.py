import re

# Leer el archivo views.py
with open('gestion/views.py', 'r') as f:
    content = f.read()

print("=== VERIFICACIÓN DE VISTAS DUPLICADAS ===\n")

# Buscar todas las definiciones de funciones
function_patterns = re.findall(r'^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', content, re.MULTILINE)

# Contar duplicados
function_counts = {}
for func in function_patterns:
    function_counts[func] = function_counts.get(func, 0) + 1

print("Funciones duplicadas:")
duplicated_functions = {func: count for func, count in function_counts.items() if count > 1}
if duplicated_functions:
    for func, count in duplicated_functions.items():
        print(f"  - {func}() aparece {count} veces")
        # Encontrar líneas donde aparece
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if re.match(rf'^def\s+{re.escape(func)}\s*\(', line):
                print(f"    * Línea {i}: {line.strip()}")
else:
    print("  ✅ No hay funciones duplicadas")

print(f"\nTotal de funciones encontradas: {len(function_patterns)}")
print(f"Total de funciones únicas: {len(set(function_patterns))}")

# Buscar decoradores @login_required duplicados o inconsistentes
login_required_pattern = r'@login_required\s*\ndef\s+([a-zA-Z_][a-zA-Z0-9_]*)'
login_required_funcs = re.findall(login_required_pattern, content)

print(f"\nFunciones con @login_required: {len(login_required_funcs)}")

# Buscar funciones sin @login_required
all_public_funcs = [f for f in function_patterns if not f.startswith('_')]
funcs_without_login = set(all_public_funcs) - set(login_required_funcs)

if funcs_without_login:
    print(f"\n⚠️  Funciones públicas SIN @login_required ({len(funcs_without_login)}):")
    for func in sorted(list(funcs_without_login))[:10]:  # Mostrar solo las primeras 10
        print(f"  - {func}()")
    if len(funcs_without_login) > 10:
        print(f"  ... y {len(funcs_without_login) - 10} más")
else:
    print("\n✅ Todas las funciones públicas tienen @login_required")
