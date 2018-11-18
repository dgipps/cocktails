from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Loads csv of Death & Co ingredients'

    def add_arguments(self, parser):
        parser.add_argument('-i', dest='filename', required=True,
                    help='input file with recipes', metavar='FILE')

    def handle(self, *args, **options):
        with open(options['filename'], 'rb') as recipes:
            for recipe in recipes:
                print(recipe)