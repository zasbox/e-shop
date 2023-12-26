from django.core.management import BaseCommand, call_command

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        call_command('loaddata', 'catalog_data.json', verbosity=0)

