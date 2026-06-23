from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
]

