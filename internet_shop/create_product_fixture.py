import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internet_shop.settings')
django.setup()

from django.core.serializers import serialize
from catalog.models import Product

products = Product.objects.all()
print(f"Найдено продуктов: {products.count()}")

if products.exists():
    data = serialize('json', products)
    with open('catalog/fixtures/product.json', 'w', encoding='utf-8') as f:
        f.write(data)
    print("Фикстура успешно создана.")
else:
    print("Нет продуктов в базе. Сначала создайте продукты.")
