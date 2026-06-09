from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Load test data (fixtures)'

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        call_command('loaddata', 'catalog/fixtures/category.json')
        call_command('loaddata', 'catalog/fixtures/product.json')
        self.stdout.write(self.style.SUCCESS('Test data loaded'))
