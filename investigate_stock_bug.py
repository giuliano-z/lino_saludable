#!/usr/bin/env python3
"""
🔍 INVESTIGAR BUG DE STOCK - Harina de Almendras
Verifica el stock real en producción
"""

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://web-production-b0ad1.up.railway.app"
USERNAME = "el_super_creador"
PASSWORD = "tiSrsgz2nBqrVLA"

print("=" * 80)
print("  🔍 INVESTIGANDO BUG DE STOCK")
print("=" * 80)

# Crear sesión
session = requests.Session()

# 1. Login
print("\n1. Haciendo login...")
response = session.get(f"{BASE_URL}/admin/login/")
csrf_token = session.cookies['csrftoken']

login_data = {
    'username': USERNAME,
    'password': PASSWORD,
    'csrfmiddlewaretoken': csrf_token,
    'next': '/admin/'
}

response = session.post(
    f"{BASE_URL}/admin/login/",
    data=login_data,
    headers={'Referer': f"{BASE_URL}/admin/login/"}
)

if response.status_code == 200 and '/admin/' in response.url:
    print("✅ Login exitoso")
else:
    print("❌ Login falló")
    exit(1)

# 2. Buscar "Harina de Almendras" en productos
print("\n2. Buscando en Admin Django - Productos...")
response = session.get(f"{BASE_URL}/admin/gestion/producto/")

soup = BeautifulSoup(response.content, 'html.parser')

# Buscar la tabla de productos
resultados = soup.find_all('tr', class_=['row1', 'row2'])
print(f"   Encontrados {len(resultados)} productos")

for row in resultados:
    nombre_cell = row.find('th', class_='field-nombre')
    if nombre_cell and 'Harina' in nombre_cell.text:
        print(f"   ✅ Encontrado: {nombre_cell.text.strip()}")
        # Buscar el link de edición
        link = nombre_cell.find('a')
        if link:
            product_url = BASE_URL + link['href']
            print(f"   📍 URL: {product_url}")
            
            # Obtener detalles del producto
            product_response = session.get(product_url)
            product_soup = BeautifulSoup(product_response.content, 'html.parser')
            
            # Buscar campo stock
            stock_input = product_soup.find('input', {'id': 'id_stock'})
            if stock_input:
                stock_value = stock_input.get('value', 'N/A')
                print(f"   📊 Stock en DB: {stock_value}")

# 3. Buscar en Materias Primas
print("\n3. Buscando en Admin Django - Materias Primas...")
response = session.get(f"{BASE_URL}/admin/gestion/materiaprima/")

soup = BeautifulSoup(response.content, 'html.parser')
resultados = soup.find_all('tr', class_=['row1', 'row2'])
print(f"   Encontrados {len(resultados)} materias primas")

for row in resultados:
    nombre_cell = row.find('th', class_='field-nombre')
    if nombre_cell and 'Harina' in nombre_cell.text:
        print(f"   ✅ Encontrado: {nombre_cell.text.strip()}")
        link = nombre_cell.find('a')
        if link:
            mp_url = BASE_URL + link['href']
            print(f"   📍 URL: {mp_url}")
            
            mp_response = session.get(mp_url)
            mp_soup = BeautifulSoup(mp_response.content, 'html.parser')
            
            stock_input = mp_soup.find('input', {'id': 'id_stock_actual'})
            if stock_input:
                stock_value = stock_input.get('value', 'N/A')
                print(f"   📊 Stock en DB: {stock_value}")

print("\n" + "=" * 80)
print("  ✅ INVESTIGACIÓN COMPLETADA")
print("=" * 80)
