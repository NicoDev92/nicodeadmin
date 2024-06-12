# Generated by Django 5.0.5 on 2024-05-16 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cmp", "0006_alter_factura_metodo_pago"),
    ]

    operations = [
        migrations.CreateModel(
            name="PagoParcial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha_pago", models.DateTimeField()),
                ("monto", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "factura",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pagos_parciales",
                        to="cmp.factura",
                    ),
                ),
            ],
        ),
    ]
