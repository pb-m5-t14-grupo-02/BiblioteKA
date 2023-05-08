from django.db import models
from core.constrains import repr_default, AUTHOR

class Author(models.Model):
    image = models.FileField(
        upload_to="authors",
        default="https://res.cloudinary.com/dnxhcbb0u/image/upload/v1683571920/defaults/author/author_rpspwb.jpg"
    )
    name = models.CharField(max_length=120)
    about = models.TextField()

    def __repr__(self) -> str:
        return repr_default(AUTHOR, self.pk, self.name)
