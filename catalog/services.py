from .models import Product, Category

def get_products_by_category(category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
        return Product.objects.filter(category=category)
    except Category.DoesNotExist:
        return Product.objects.none()
