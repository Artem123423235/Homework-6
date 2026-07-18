from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'is_published']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'image': 'Изображение',
            'is_published': 'Опубликовано',
        }

