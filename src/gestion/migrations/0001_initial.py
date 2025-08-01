# Generated by Django 5.2.4 on 2025-07-22 22:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateField(auto_now_add=True)),
                ('proveedor', models.CharField(max_length=100)),
                ('materia_prima', models.CharField(help_text='Ej: Pistachos a granel', max_length=200)),
                ('cantidad_mayoreo', models.DecimalField(decimal_places=2, help_text='Cantidad en kilos', max_digits=10)),
                ('precio_mayoreo', models.DecimalField(decimal_places=2, help_text='Precio total de la compra', max_digits=10)),
                ('precio_unitario_mayoreo', models.DecimalField(decimal_places=2, editable=False, help_text='Precio por kilo (calculado automáticamente)', max_digits=10)),
                ('stock_mayoreo', models.DecimalField(decimal_places=2, help_text='Stock disponible para racionar', max_digits=10)),
            ],
            options={
                'verbose_name': 'Compra al Mayoreo',
                'verbose_name_plural': 'Compras al Mayoreo',
                'ordering': ['-fecha_compra'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(default=0)),
                ('categoria', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_minimo', models.IntegerField(default=5, help_text='Stock mínimo antes de alerta')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.producto')),
            ],
            options={
                'verbose_name_plural': 'Ventas',
            },
        ),
    ]
