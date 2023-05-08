# Generated by Django 4.2 on 2023-05-08 20:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                        default="https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683571920/defaults/author/author_rpspwb.jpg",
                        upload_to="authors",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("about", models.TextField()),
            ],
        ),
    ]