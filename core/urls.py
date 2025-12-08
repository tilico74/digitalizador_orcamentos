from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('orc_listar/', views.orc_listar, name='orc_listar'),
    path('teste-orcamentos/', views.teste_orcamentos, name='teste_orcamentos'),
]