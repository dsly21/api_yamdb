import csv

from django.core.management.base import BaseCommand

from api.models import Genres, GenreTitle, Titles


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/genre_title.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                title_id = Titles.objects.get(pk=row[1])
                genre_id = Genres.objects.get(pk=row[2])

                genretitle = GenreTitle(
                    id=row[0], title=title_id, genre=genre_id
                )
                genretitle.save()
