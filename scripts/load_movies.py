import csv

from datetime import datetime, timedelta

from movies.models import MovieModel, ProgramModel

def restore_coma(string:str):
    if '-' in string:
        return string.replace('-', ',')
    return string


# Create movies
with open('scripts/Movies_data.csv') as file:
    reader = csv.reader(file)

    for id, row in enumerate(reader):
        data = row[0].split(';')
        movie =MovieModel.objects.create(
            title=data[0],
            description = restore_coma(data[1]),
            trailer_link = data[2],
            category = restore_coma(data[3]),
            duration = data[4],
            age_category = data[5],
            cast = restore_coma(data[6]),
            release_date = data[7],
            direction = restore_coma(data[8]),
            script = restore_coma(data[9]),
            poster = f'preload_posters/{id}.jpg'
        )
        print(f'Created movie: {data[0]}')

# Create movie sessions for today and next two days
movies = MovieModel.objects.all()

for counter, movie in enumerate(movies):
    if counter <=3:
        ProgramModel.objects.create(movie=movie, date=datetime.now(), price=9.99)
    elif counter <= 7:
        ProgramModel.objects.create(movie=movie, date=datetime.now()+timedelta(days=1), price=9.99)
    else:
        ProgramModel.objects.create(movie=movie, date=datetime.now()+timedelta(days=2), price=9.99)