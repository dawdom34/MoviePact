# Generated by Django 4.1.7 on 2023-03-28 09:58

from django.db import migrations, models
import movies.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_moviemodel_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviemodel',
            name='poster',
            field=models.ImageField(default='default-movie-poster.jpg', upload_to=movies.models.poster_filepath),
        ),
    ]