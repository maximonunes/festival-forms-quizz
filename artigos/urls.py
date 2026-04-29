from django.urls import path
from . import views

app_name = 'artigos'  # Importante para o {% url 'artigos:lista_artigos' %}

urlpatterns = [
    path('', views.lista_artigos, name='lista_artigos'),
    path('like/<int:artigo_id>/', views.like_artigo, name='like_artigo'),
]