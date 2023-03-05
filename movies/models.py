from django.db import models


def poster_filepath(self, *args, **kwargs):
    return f'posters/{str(self.title)}.jpg'



class MovieModel(models.Model):
    title = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    trailer_link = models.CharField(max_length=255)
    category = models.CharField(max_length=200)
    duration = models.IntegerField()
    age_category = models.SmallIntegerField()
    cast = models.TextField()
    release_date = models.DateField()
    direction = models.CharField(max_length=200)
    script = models.CharField(max_length=200)
    poster = models.ImageField(upload_to=poster_filepath)

    def __str__(self) -> str:
        return self.title