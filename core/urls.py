from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('orc_listar/', views.orc_listar, name='orc_listar'),
    path('orc_insere/', views.orc_insere, name='orc_insere'),
    path('orc_excluir/<int:id_orc>/', views.orc_excluir, name='orc_excluir'),
    path('orc_editar/<int:id_orc>/', views.orc_editar, name='orc_editar'),
    path('orc_pdf/<int:id_orc>/', views.orc_pdf, name='orc_pdf'),
    path('desc_listar/', views.desc_listar, name='desc_listar'),
    path('desc_insere/', views.desc_insere, name='desc_insere'),
    path('desc_excluir/<int:id_desc>/', views.desc_excluir, name='desc_excluir'),
    path('desc_editar/<int:id_desc>/', views.desc_editar, name='desc_editar'),
]