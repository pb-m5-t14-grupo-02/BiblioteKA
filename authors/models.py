from django.db import models
from core.constrains import repr_default, AUTHOR

class Author(models.Model):
    image = models.TextField(default="https://i.postimg.cc/QCYpJHRc/person-placeholder.jpg")
    name = models.CharField(max_length=120)
    about = models.TextField()

    def __repr__(self) -> str:
        return repr_default(AUTHOR, self.pk, self.name)
