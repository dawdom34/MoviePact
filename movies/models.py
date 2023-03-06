from django.db import models

from users.models import UserModel


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
    

class ProgramModel(models.Model):
    """
    Sessions set for a specific day and time
    """
    movie = models.ForeignKey(MovieModel, on_delete=models.RESTRICT)
    date = models.DateTimeField()
    price = models.FloatField()

    def __str__(self) -> str:
        return self.movie.title


class SeatsModel(models.Model):
    """
    Seat reservation
    """
    program = models.ForeignKey(ProgramModel, on_delete=models.RESTRICT)
    seats_numbers = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.seats_numbers


class TicketsModel(models.Model):
    """
    Tickets
    """
    program = models.ForeignKey(ProgramModel, on_delete=models.RESTRICT)
    user = models.ForeignKey(UserModel, on_delete=models.RESTRICT)
    seats = models.ForeignKey(SeatsModel, on_delete=models.CASCADE)