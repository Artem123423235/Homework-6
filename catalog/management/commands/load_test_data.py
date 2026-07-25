from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load test data from fixtures'

    def handle(self, *args, **options):
        call_command('loaddata', 'catalog/fixtures/category.json')
        call_command('loaddata', 'catalog/fixtures/product.json')
        self.stdout.write(self.style.SUCCESS('Test data loaded successfully'))
