# Generated by Django 4.2.1 on 2023-05-09 14:52

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
                    models.FileField(
                        default="https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683571699/defaults/book/book_kzgg3h.png",
                        upload_to="books",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("series", models.CharField(default=None, max_length=120, null=True)),
                ("genre", models.CharField(default=None, max_length=120, null=True)),
                ("about", models.TextField()),
                ("year", models.IntegerField()),
                (
                    "days",
                    models.IntegerField(
                        choices=[(7, "Week"), (15, "Fortnight"), (30, "Month")],
                        default=7,
                    ),
                ),
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
                ("is_avaliable", models.BooleanField(default=True)),
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
                ("load_date", models.DateField(auto_now_add=True)),
                ("return_date", models.DateField()),
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
