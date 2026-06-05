from django.shortcuts import render

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
