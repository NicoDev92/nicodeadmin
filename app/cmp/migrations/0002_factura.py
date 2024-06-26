# Generated by Django 5.0.5 on 2024-05-14 16:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cmp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Factura",
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
                ("estado", models.BooleanField(default=True)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("fecha_modificacion", models.DateTimeField(auto_now=True)),
                ("usuario_modifica", models.IntegerField(blank=True, null=True)),
                ("fecha_vencimiento", models.DateTimeField()),
                ("fecha_emision", models.DateTimeField()),
                ("esta_pago", models.BooleanField(default=False)),
                (
                    "descuento",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "impuestos",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "total_con_impuestos",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("notas", models.TextField(blank=True, null=True)),
                (
                    "numero_orden_compra",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("total_pagar", models.CharField(max_length=20)),
                ("numero_factura", models.CharField(max_length=20)),
                (
                    "metodo_pago",
                    models.CharField(
                        choices=[
                            ("efectivo", "Efectivo"),
                            ("transferecia", "Transferencia"),
                            ("debito", "Débito"),
                            ("credito", "Crédito"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "estado_factura",
                    models.CharField(
                        choices=[
                            ("emitida", "Emitida"),
                            ("pendiente", "Pendiente de Pago"),
                            ("pagada", "Pagada"),
                            ("vencida", "Vencida"),
                        ],
                        default="emitida",
                        max_length=20,
                    ),
                ),
                (
                    "proveedor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cmp.proveedor"
                    ),
                ),
                (
                    "usuario_creador",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Facturas",
            },
        ),
    ]
