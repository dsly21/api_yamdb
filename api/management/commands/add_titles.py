import csv

from api.models import Title, Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/titles.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                category = Category.objects.get(pk=row[3])
                title = Title(
                    id=row[0], name=row[1], year=row[2], category=category
                )
                title.save()
