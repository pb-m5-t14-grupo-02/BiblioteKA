# Generated by Django 4.2 on 2023-05-08 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.FileField(default='https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683571699/defaults/book/book_kzgg3h.png', upload_to='books'),
        ),
    ]
