from django.db import models

class Author(models.Model):
    image = models.TextField(default="https://i.postimg.cc/QCYpJHRc/person-placeholder.jpg")
    name = models.CharField(max_length=120)
    about = models.TextField()