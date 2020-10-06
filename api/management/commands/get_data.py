import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_names = [fn[:-3] for fn in os.listdir('./api/management/commands/')
                      if fn.startswith('add_')]
        for file in file_names:
            if file == 'add_genretitle':
                continue
            os.system('python manage.py {}'.format(file))

        os.system('python manage.py add_genretitle')
