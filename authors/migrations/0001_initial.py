# Generated by Django 4.2 on 2023-05-03 17:28

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
                    models.TextField(
                        default="https://i.postimg.cc/QCYpJHRc/person-placeholder.jpg"
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                ("about", models.TextField()),
            ],
        ),
    ]
