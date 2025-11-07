# Generated manually on 2025-11-07 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_ajusteinventario'),
    ]

    operations = [
        # Constraint para Producto: stock >= 0
        migrations.AddConstraint(
            model_name='producto',
            constraint=models.CheckConstraint(
                check=models.Q(stock__gte=0),
                name='producto_stock_no_negativo'
            ),
        ),
        # Constraint para MateriaPrima: stock_actual >= 0
        migrations.AddConstraint(
            model_name='materiaprima',
            constraint=models.CheckConstraint(
                check=models.Q(stock_actual__gte=0),
                name='mp_stock_no_negativo'
            ),
        ),
    ]
