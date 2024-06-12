# Generated by Django 5.0.5 on 2024-05-08 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inv", "0002_subcategoria"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Marca",
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
                (
                    "descripcion",
                    models.CharField(
                        help_text="Descriopción de la categoría",
                        max_length=100,
                        unique=True,
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
                "verbose_name_plural": "Marca",
            },
        ),
    ]
