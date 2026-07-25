from django.contrib import admin
from catalog.models import Product  # Убрали Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_published', 'owner')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')

