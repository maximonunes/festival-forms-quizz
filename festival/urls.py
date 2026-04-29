from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dias/', views.dias_view, name='dias'),
    path('palcos/', views.palcos_view, name='palcos'),
    
    # Detalhe e Edição de Concertos
    path('concertos/<int:concerto_id>/', views.concerto_view, name='concerto'),
    path('concertos/<int:concerto_id>/editar/', views.editar_concerto_view, name='editar_concerto'),
    
    # NOVAS ROTAS PARA CONCERTOS
    # Rota para o link "Criar concerto" no menu
    path('concertos/criar/', views.criar_concerto_view, name='criar_concerto'),
    # Rota para o botão de apagar concerto
    path('concertos/<int:concerto_id>/apagar/', views.apagar_concerto_view, name='apagar_concerto'),

    # NOVA ROTA PARA PALCOS
    # Rota para o botão "Editar palco" na página de palcos
    path('palcos/<int:palco_id>/editar/', views.editar_palco_view, name='editar_palco'),
]