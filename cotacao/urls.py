# # cotacao/urls.py
# from django.urls import path
# from . import views 


# cotacao/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # Rotas de Layout/Gerais
    path('register/', views.em_desenvolvimento_view, name='register'),
    path('configuracao/', views.em_desenvolvimento_view, name='configuracao'),
    path('usuarios/', views.em_desenvolvimento_view, name='cadastro_usuarios'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 


    # Rotas Cadastro Clientes 
    path('cadastro/cliente/', views.cadastro_cliente_view, name='cadastro_cliente'), 
    path('lista/clientes', views.lista_clientes_view, name='lista_clientes'),
    path('gerar-clientes-teste/', views.gerar_clientes_teste_view, name='gerar_clientes_teste'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente_view, name='editar_cliente'),


    # Rotas de Cotação
    path('cotacao/spots/', views.em_desenvolvimento_view, name='cotacao_spots'),
    
    # Rotas de Cotação BID
    path('cotacao/bid/', views.cotacao_bid_listagem_view, name='cotacao_bid_listagem'),
    path('api/cliente/search/',views.api_search_clients_view, name='api_search_clients'),
    path ('setup/tabela-antt/inicializar/', views.inicializar_tabelas_antt_view, name='inicializar'),
    path('api/antt/search/', views.api_search_antt_view, name='api_search_antt'),
    path('cotacao/bid/nova/', views.cotacao_bid_nova_view, name='cotacao_bid_nova'),
    path('cotacao/bid/prosseguir/', views.proxima_etapa_bid_view, name='proxima_etapa_bid'), 
    path('cotacao/bid/detalhe/<str:bid_id>/', views.cotacao_bid_detalhe_view, name='cotacao_bid_detalhe'),
    path('bid/<int:bid_id>/editar/<int:rota_id>/', views.cotacao_bid_editar_round_view, name='cotacao_bid_editar_round'),
    path('cotacao/bid/listagem', views.exibir_cotacoes_view, name='cotacao_bid_listagem'),
    path('bid/<int:bid_id>/destaque/', views.alternar_destaque_bid, name='cotacao_bid_destaque'),
    path('bid/<int:bid_id>/upload/preview/', views.upload_rotas_preview, name='upload_rotas_preview'),
    path('bid/<int:bid_id>/upload/importar/', views.upload_rotas_importar, name='upload_rotas_importar'),


    # Rota existente para o detalhe
    path('cotacao/bid/detalhe/<int:bid_id>/', views.cotacao_bid_detalhe_view, name='cotacao_bid_detalhe'),
    #path('cotacao/bid/<int:bid_id>/', views.cotacao_bid_detalhe_alt_view, name='cotacao_bid_detalhe_alt'),
    
    # ROTA NOVA E FALTANTE: Cotação em Lote por Round (Nome: cotacao_round_lote)
    path('cotacao/bid/cotar/<int:bid_id>/<str:round_name>/', 
        views.cotacao_round_lote_view, 
        name='cotacao_round_lote'),

    # ROTA QUE FALTAVA: Permite editar um round específico
    path('cotacao/bid/editar/<int:bid_id>/<int:rota_id>/', 
        views.cotacao_bid_editar_round_view, 
        name='cotacao_bid_editar_round'),







]