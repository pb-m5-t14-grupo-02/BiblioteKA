# Generated by Django 4.2.1 on 2023-05-04 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                (
                    "image",
                    models.TextField(
                        default="https://i.postimg.cc/J7H4ryhJ/51s-Is-L2-Hpp-L-SX337-BO1-204-203-200-cleanup.png"
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("series", models.CharField(default=None, max_length=120, null=True)),
                ("genre", models.CharField(default=None, max_length=120, null=True)),
                ("about", models.TextField()),
                ("year", models.IntegerField()),
                ("ISBN", models.CharField(default=None, max_length=13, null=True)),
                ("ASIN", models.CharField(default=None, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Copy",
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
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="copies",
                        to="books.book",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookLoan",
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
                ("load_date", models.DateTimeField(auto_now_add=True)),
                ("return_date", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "copy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.copy"
                    ),
                ),
            ],
        ),
    ]
