from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts/', views.contacts, name='contacts'),
]
