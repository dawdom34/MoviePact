from django.db import models

from users.models import UserModel

#from embed_video.fields import EmbedVideoFiled

def poster_filepath(self, *args, **kwargs):
    """
    Posters upload path
    """
    return f'posters/{str(self.title)}.jpg'



class MovieModel(models.Model):
    """
    Movies and information about them
    """
    title = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    trailer_link = models.URLField()
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
    

class ProgramModel(models.Model):
    """
    Sessions set for a specific day and time
    """
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.movie.title


class SeatsModel(models.Model):
    """
    Seat reservation
    """
    program = models.ForeignKey(ProgramModel, on_delete=models.CASCADE)
    seats_numbers = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.seats_numbers


class TicketsModel(models.Model):
    """
    Tickets
    """
    program = models.ForeignKey(ProgramModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    seats = models.ForeignKey(SeatsModel, on_delete=models.CASCADE)