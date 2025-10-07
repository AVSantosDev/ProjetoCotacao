# # cotacao/urls.py
# from django.urls import path
# from . import views 


# cotacao/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # Rotas de Layout/Gerais
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'), 
    path('configuracao/', views.configuracao_view, name='configuracao'),
    path('usuarios/', views.cadastro_usuarios_view, name='cadastro_usuarios'),
    path('dashboard/', views.dashboard_view, name='dashboard'),


    # Rotas Cadastro Clientes 
    path('cadastro/cliente/', views.cadastro_cliente_view, name='cadastro_cliente'), 
    path('lista/clientes', views.lista_clientes_view, name='lista_clientes'),
    path('gerar-clientes-teste/', views.gerar_clientes_teste_view, name='gerar_clientes_teste'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente_view, name='editar_cliente'),


    # Rotas de Cotação
    path('cotacao/spots/', views.cotacao_spots_view, name='cotacao_spots'),
    
    # Rotas de Cotação BID
    path('cotacao/bid/', views.cotacao_bid_listagem_view, name='cotacao_bid_listagem'),
    path('api/cliente/search/',views.api_search_clients_view, name='api_search_clients'),
    path ('setup/tabela-antt/inicializar/', views.inicializar_tabelas_antt_view, name='inicializar'),
    path('api/antt/search/', views.api_search_antt_view, name='api_search_antt'),
    path('cotacao/bid/nova/', views.cotacao_bid_nova_view, name='cotacao_bid_nova'),
    path('cotacao/bid/prosseguir/', views.proxima_etapa_bid_view, name='proxima_etapa_bid'), 
    path('cotacao/bid/detalhe/<int:bid_id>/', views.cotacao_bid_detalhe_view, name='cotacao_bid_detalhe'),
    path('bid/<int:bid_id>/editar/<int:rota_id>/', views.cotacao_bid_editar_round_view, name='cotacao_bid_editar_round'),

    # Rota existente para o detalhe
    path('cotacao/bid/detalhe/<int:bid_id>/', views.cotacao_bid_detalhe_view, name='cotacao_bid_detalhe'),
    
    # ROTA NOVA E FALTANTE: Cotação em Lote por Round (Nome: cotacao_round_lote)
    path('cotacao/bid/cotar/<int:bid_id>/<str:round_name>/', 
        views.cotacao_round_lote_view, 
        name='cotacao_round_lote'),

    # ROTA QUE FALTAVA: Permite editar um round específico
    path('cotacao/bid/editar/<int:bid_id>/<int:rota_id>/', 
        views.cotacao_bid_editar_round_view, 
        name='cotacao_bid_editar_round'),







]