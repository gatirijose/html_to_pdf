# Generated by Django 4.2 on 2023-06-27 19:50

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
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
                ("title", models.CharField(max_length=200)),
                ("content", tinymce.models.HTMLField()),
                ("date_created", models.DateField(auto_now_add=True)),
            ],
        ),
    ]
