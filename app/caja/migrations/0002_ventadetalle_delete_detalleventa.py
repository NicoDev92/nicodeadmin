# Generated by Django 5.0.5 on 2024-05-18 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("caja", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VentaDetalle",
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
                ("producto", models.CharField(max_length=100)),
                (
                    "precio_unitario",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("cantidad", models.FloatField()),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "venta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="caja.venta"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="DetalleVenta",
        ),
    ]
