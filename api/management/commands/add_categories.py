import csv

from api.models import Categories
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/category.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                category = Categories(id=row[0], name=row[1], slug=row[2])
                category.save()
