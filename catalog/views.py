from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import permission_required
from .models import Product
from .forms import ProductForm
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import Product, Category
from .services import get_products_by_category
from django.core.cache import cache
from django.views.generic import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        # Пытаемся получить кеш
        queryset = cache.get('all_products')
        if queryset is None:
            queryset = Product.objects.all()
            cache.set('all_products', queryset, 60 * 5)   # кеш на 5 минут
        return queryset

class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return get_products_by_category(slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(slug=self.kwargs.get('slug')).first()
        return context


# --- Отмена публикации (только модератор) ---
@permission_required('catalog.can_unpublish_product')
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_detail', pk=pk)


# --- Главная страница (список продуктов) ---
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    ordering = ['-id']

# --- Детальная страница продукта ---
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# --- Создание продукта (только авторизованные) ---
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# --- Редактирование продукта (только владелец или модератор) ---
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_unpublish_product'))


# --- Удаление продукта (только владелец или модератор) ---
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_unpublish_product'))


# --- Страница контактов ---
class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    @cache_page(60 * 15)  # кеш на 15 минут
    def product_detail(request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'catalog/product_detail.html', {'product': product})
