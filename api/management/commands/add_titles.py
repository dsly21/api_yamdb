import csv

from django.core.management.base import BaseCommand

from api.models import Categories, Titles


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/titles.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                category = Categories.objects.get(pk=row[3])
                title = Titles(
                    id=row[0], name=row[1], year=row[2], category=category
                )
                title.save()
