# seu_projeto/urls.py (o arquivo principal)
from django.contrib import admin
from django.urls import path, include
from cotacao.views import login_view


urlpatterns = [
    #1 primeira tela
    path('', login_view, name='login'),
    
    #2 segunda tela
    path('dashboard', include('cotacao.urls')),

    # Se você usava 'cotacao/' como home, agora ele aponta para a aplicação
    path('cotacao/', include('cotacao.urls')),
    
    path('admin/', admin.site.urls),
    
]