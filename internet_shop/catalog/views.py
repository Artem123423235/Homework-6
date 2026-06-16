from django.shortcuts import render, get_object_or_404
from catalog.models import Product

def index(request):
    context = {
        'title': 'Главная',
        'header': 'Добро пожаловать в наш интернет-магазин!',
        'description': 'Лучшие товары по лучшим ценам.',
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'catalog/contacts.html', context)

def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
