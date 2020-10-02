import csv

from django.core.management.base import BaseCommand

from api.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/users.csv', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for id, row in enumerate(spamreader):
                if id == 0:
                    continue
                # if row[3] == 'admin':
                #     user = User(id=row[0], username=row[1], email=row[2], is_superuser=True)
                # elif row[3] == 'moderator':
                #     user = User(id=row[0], username=row[1], email=row[2], is_staff=True)
                # else:
                user = User(id=row[0], username=row[1], email=row[2], role=row[3])
                user.save()
