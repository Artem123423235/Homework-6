import os
from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image', 'category']  # category добавлено

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей (Bootstrap)
        for field_name, field in self.fields.items():
            if field_name in ('title', 'description', 'price', 'category'):
                field.widget.attrs['class'] = 'form-control'
            elif field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'

    # Валидация названия (запрещённые слова)
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title_lower = title.lower()
            for word in FORBIDDEN_WORDS:
                if word in title_lower:
                    raise ValidationError(f'Название не должно содержать слово "{word}".')
        return title

    # Валидация описания (запрещённые слова)
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise ValidationError(f'Описание не должно содержать слово "{word}".')
        return description

    # Валидация цены (неотрицательная)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    # Валидация изображения (доп. задание)
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Размер (5 MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Изображение не должно превышать 5 МБ.')
            # Формат
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_extensions:
                raise ValidationError('Допустимы только файлы JPEG и PNG.')
        return image
