from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]

urlpatterns = [
    path('', views.home, name='home'),                     # главная (ещё не создали)
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # страница товара
]
