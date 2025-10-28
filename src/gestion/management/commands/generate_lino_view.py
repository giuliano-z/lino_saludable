"""
Generador automático de vistas usando el patrón LINO
Uso: python manage.py generate_lino_view compras --model=Compra --title="Gestión de Compras"
"""
from django.core.management.base import BaseCommand
from django.template import Template, Context
from pathlib import Path

class Command(BaseCommand):
    help = 'Genera una vista completa usando el patrón LINO'
    
    def add_arguments(self, parser):
        parser.add_argument('view_name', type=str, help='Nombre de la vista (ej: compras)')
        parser.add_argument('--model', type=str, help='Nombre del modelo Django')
        parser.add_argument('--title', type=str, help='Título de la vista')
        parser.add_argument('--icon', type=str, default='bi-list', help='Ícono Bootstrap')
        parser.add_argument('--color', type=str, default='green', help='Color del tema LINO')
    
    def handle(self, *args, **options):
        view_name = options['view_name']
        model_name = options.get('model', view_name.capitalize())
        title = options.get('title', f'Gestión de {view_name.capitalize()}')
        icon = options['icon']
        color = options['color']
        
        self.stdout.write(f'🚀 Generando vista LINO: {view_name}')
        
        # Template base optimizado
        template_content = """{% extends 'gestion/base.html' %}
{% load dietetica_tags %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <!-- Hero Section con gradiente LINO -->
    <div class="position-relative overflow-hidden mb-4">
        <div class="bg-gradient-{{ color }} text-white rounded-4 shadow-lg">
            <div class="container-fluid p-4">
                <div class="row align-items-center">
                    <div class="col-lg-9">
                        <div class="d-flex align-items-center mb-3">
                            {% lino_icon "{{ icon }}" "fs-2 me-3" %}
                            <div>
                                <h1 class="h3 mb-0 fw-bold">{{ title }}</h1>
                                <p class="mb-0 opacity-75">Gestión optimizada con componentes LINO</p>
                            </div>
                        </div>
                        
                        <!-- KPIs integrados -->
                        <div class="row text-center">
                            <div class="col-3">
                                <div class="text-center">
                                    <div class="bg-white bg-opacity-15 rounded-3 p-2 mb-1">
                                        {% lino_icon "bi-check-circle" "text-white fs-6" %}
                                    </div>
                                    <div class="text-white fw-bold fs-6">{{ total_activos|default:"0" }}</div>
                                    <small class="text-white opacity-75">Activos</small>
                                </div>
                            </div>
                            <!-- Más KPIs aquí -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- KPIs usando componentes LINO -->
    <div class="lino-grid lino-grid--4-col mb-4">
        {% lino_kpi_card "Total" total "Registros totales" "{{ icon }}" "{{ color }}" %}
        <!-- Más KPIs personalizables -->
    </div>

    <!-- Panel de Control -->
    <div class="row mb-3">
        <div class="col-xl-8 col-lg-7 mb-4">
            {% lino_search_panel "Panel de Control" "Buscar..." %}
        </div>
        
        <div class="col-xl-4 col-lg-5">
            <!-- Acciones rápidas -->
            <div class="card border-0 shadow-sm h-100">
                <div class="card-body p-4">
                    {% lino_card_header "Acciones Rápidas" "bi-lightning-charge" "warning" %}
                    <div class="d-grid gap-2">
                        {% lino_button "Crear Nuevo" "success" "bi-plus-circle" %}
                        {% lino_button "Exportar" "outline-secondary" "bi-download" %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabla de datos -->
    <div class="card border-0 shadow-sm">
        <div class="card-body p-0">
            <!-- Contenido de la tabla aquí -->
        </div>
    </div>
{% endblock %}"""
        
        # Crear el archivo de template
        template_dir = Path('src/gestion/templates/modules') / view_name
        template_dir.mkdir(parents=True, exist_ok=True)
        
        template_file = template_dir / f'lista_{view_name}.html'
        
        # Renderizar el template
        template = Template(template_content)
        context = Context({
            'title': title,
            'icon': icon,
            'color': color,
            'view_name': view_name
        })
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template.render(context))
        
        self.stdout.write(self.style.SUCCESS(f'✅ Vista generada: {template_file}'))
        
        # Mostrar próximos pasos
        self.stdout.write(self.style.WARNING('\n📋 Próximos pasos:'))
        self.stdout.write(f'1. Agregar la vista en views.py')
        self.stdout.write(f'2. Configurar la URL en urls.py')
        self.stdout.write(f'3. Personalizar los KPIs específicos')
        self.stdout.write(f'4. Implementar la lógica de filtros')
