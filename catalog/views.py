from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm
from .models import Category, Product


CACHE_ENABLED = getattr(settings, "CACHE_ENABLED", False)


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    ordering = ["-id"]


@method_decorator(
    cache_page(60 * 15) if CACHE_ENABLED else (lambda view: view),
    name="dispatch",
)
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductsByCategoryView(ListView):
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        # Если у Product есть ForeignKey/ManyToMany к Category
        # с именем поля category:
        return Product.objects.filter(
            category__slug=slug
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = Category.objects.filter(
            slug=self.kwargs.get("slug")
        ).first()

        return context


@permission_required("catalog.can_unpublish_product")
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save(update_fields=["is_published"])

    return redirect("catalog:product_detail", pk=pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()

        return (
            self.request.user == product.owner
            or self.request.user.has_perm(
                "catalog.can_unpublish_product"
            )
        )


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        product = self.get_object()

        return (
            self.request.user == product.owner
            or self.request.user.has_perm(
                "catalog.can_unpublish_product"
            )
        )


class ContactView(TemplateView):
    template_name = "catalog/contacts.html"
