# Generated by Django 5.0.5 on 2024-05-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inv", "0008_remove_producto_precio_compra_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="producto",
            name="precio_venta",
            field=models.FloatField(blank=True, null=True),
        ),
    ]