import re

# Leer el archivo urls.py
with open('gestion/urls.py', 'r') as f:
    content = f.read()

# Buscar todos los patrones de URLs
url_patterns = re.findall(r"path\('([^']+)'.*name='([^']+)'\)", content)

print("=== VERIFICACIÓN DE URLs DUPLICADAS ===\n")

# Verificar URLs duplicadas
urls = [pattern[0] for pattern in url_patterns]
url_counts = {}
for url in urls:
    url_counts[url] = url_counts.get(url, 0) + 1

print("URLs duplicadas:")
duplicated_urls = {url: count for url, count in url_counts.items() if count > 1}
if duplicated_urls:
    for url, count in duplicated_urls.items():
        print(f"  - '{url}' aparece {count} veces")
else:
    print("  ✅ No hay URLs duplicadas")

print()

# Verificar nombres duplicados
names = [pattern[1] for pattern in url_patterns]
name_counts = {}
for name in names:
    name_counts[name] = name_counts.get(name, 0) + 1

print("Nombres duplicados:")
duplicated_names = {name: count for name, count in name_counts.items() if count > 1}
if duplicated_names:
    for name, count in duplicated_names.items():
        print(f"  - '{name}' aparece {count} veces")
else:
    print("  ✅ No hay nombres duplicados")

print()
print(f"Total de URLs encontradas: {len(urls)}")
print(f"Total de nombres únicos: {len(set(names))}")
