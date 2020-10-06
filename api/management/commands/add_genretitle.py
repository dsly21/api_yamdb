import csv

from api.models import Genre, Title
from django.core.management.base import BaseCommand

from api.models import Genres, GenreTitle, Titles


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/genre_title.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                title = Title.objects.get(pk=row[1])
                genre = Genre.objects.get(pk=row[2])

                title.genre.add(genre)
