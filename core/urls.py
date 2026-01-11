from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('orc_listar/', views.orc_listar, name='orc_listar'),
    path('orc_insere_index/', views.orc_insere_index, name='orc_insere_index'),
    path("orc_insere/<str:tipo>/", views.orc_insere, name="orc_insere"),
    path('orc_excluir/<int:id_orc>/', views.orc_excluir, name='orc_excluir'),
    path('orc_editar/<int:id_orc>/', views.orc_editar, name='orc_editar'),
    path('orc_pdf/<int:id_orc>/', views.orc_pdf, name='orc_pdf'),
    path('desc_listar/', views.desc_listar, name='desc_listar'),
    path('desc_insere/', views.desc_insere, name='desc_insere'),
    path('desc_excluir/<int:id_desc>/', views.desc_excluir, name='desc_excluir'),
    path('desc_editar/<int:id_desc>/', views.desc_editar, name='desc_editar'),
    path("desc_pesquisar/", views.desc_pesquisar, name="desc_pesquisar"),
    path('cond_listar/', views.cond_listar, name='cond_listar'),
    path('cond_insere/', views.cond_insere, name='cond_insere'),
    path('cond_excluir/<int:id_cond>/', views.cond_excluir, name='cond_excluir'),
    path('cond_editar/<int:id_cond>/', views.cond_editar, name='cond_editar'),
    path("cond_pesquisar/", views.cond_pesquisar, name="cond_pesquisar"),
]