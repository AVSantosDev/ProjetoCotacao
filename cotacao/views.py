# cotacao/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse

# --- DEFINIÇÃO DO MOCK DE DADOS ---
# Use uma lista de dicionários para simular o banco de dados.
# O MOCK precisa ter um ID único para funcionar corretamente.
rotas_mock = [
    # MOCK de dados para rotas na listagem de detalhes do BID
    {'id': 1, 'bid_id': 1001, 'cod': 'BID-1001-A', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'São Paulo - SP', 'destino': 'Rio de Janeiro - RJ', 'veiculo': 'Caminhão', 'eixos': 5, 'R1': 'R$ 3.800,00', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 900},
    {'id': 2, 'bid_id': 1001, 'cod': 'BID-1001-B', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'Curitiba - PR', 'destino': 'Florianópolis - SC', 'veiculo': 'Carreta LS', 'eixos': 6, 'R1': 'R$ 1.950,00', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 300},
    {'id': 3, 'bid_id': 1001, 'cod': 'BID-1001-C', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'Curitiba - PR', 'destino': 'Porto Alegre - RS', 'veiculo': 'VUC', 'eixos': 2, 'R1': 'R$ 2.100', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 700},
    # Adicionando um BID diferente para teste
    {'id': 4, 'bid_id': 1002, 'cod': 'BID-1002-D', 'grupo': 'G-100', 'origem': 'Recife - PE', 'destino': 'Natal - RN', 'veiculo': 'Truck', 'eixos': 3, 'R1': '-', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 300},
]
# ---------------------------------------------------------

# --- FUNÇÃO AUXILIAR MOCK PARA BUSCAR ROTAS ---
def get_rotas_for_bid(bid_id):
    """ Filtra rotas_mock pelo bid_id. """
    return [r for r in rotas_mock if r['bid_id'] == bid_id]

# --- FUNÇÃO AUXILIAR MOCK PARA OBTER DADOS DE ROTA ---
def get_rota_by_id(rota_id):
    """ Busca uma rota pelo ID. """
    for rota in rotas_mock:
        if rota['id'] == rota_id:
            return rota
    return None

# --- FUNÇÃO AUXILIAR PARA OBTER PREÇO DO ROUND ---
def get_round_price(rota, round_name):
    """ Simula o método get_round_price do template cotacao_round_lote.html. """
    return rota.get(round_name, '-')
# -------------------------------------------------


# VIEWS GERAIS
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == 'admin':
            return redirect('dashboard')
        else:
            context ={
                'error_message':'Credenciais ínvalidas. Tente novamente!'
            } 
            return render(request,'login.html', context)

    return render(request, 'login.html', {})

def register_view(request):
    return render(request, 'register.html', {})

def logout_view(request):
    return redirect('login') 

def configuracao_view(request):
    return render(request, 'configuracao.html', {})

def cadastro_usuarios_view(request):
    return render(request, 'cadastro_usuarios.html', {})

# DASHBOARD
def dashboard_view(request):
    return render(request, 'dashboard.html', {})

# COTAÇÃO SPOT (Placeholder)
def cotacao_spots_view(request):
    return render(request, 'cotacao_spots.html', {})

# COTAÇÃO BID (Fluxo completo)
def cotacao_bid_listagem_view(request):
    return render(request, 'cotacao_bid_listagem.html', {})

def cotacao_bid_nova_view(request):
    return render(request, 'cotacao_bid_nova.html', {})

def proxima_etapa_bid_view(request):
    """ Processa o formulário inicial e redireciona para a tela de detalhe. """
    if request.method == 'POST':
        # MOCK: Assumindo que o novo BID ID é 1002 para o exemplo
        novo_bid_id = 1002 
        # 🚨 CORREÇÃO: Removido 'cotacao:'
        return redirect('cotacao_bid_detalhe', bid_id=novo_bid_id)
    # 🚨 CORREÇÃO: Removido 'cotacao:'
    return redirect('cotacao_bid_nova')


def cotacao_bid_detalhe_view(request, bid_id):
    """ Renderiza a tela de detalhes do BID (tabela de rotas, cálculos, rounds). """
    rotas_filtradas = get_rotas_for_bid(bid_id)
    
    context = {
        'bid_id': bid_id,
        'rotas': rotas_filtradas,
    }
    return render(request, 'cotacao_bid_detalhe.html', context)


def cotacao_bid_editar_round_view(request, bid_id, rota_id):
    """ Simula o processamento do formulário de edição de round e redireciona de volta. """
    if request.method == 'POST':
        rota = get_rota_by_id(rota_id)

        if not rota:
            # 🚨 CORREÇÃO: Removido 'cotacao:'
            return redirect('cotacao_bid_detalhe', bid_id=bid_id) 
            
        round_name = request.POST.get('round_name')
        km_value = request.POST.get('km_value')
        percentage_increase = request.POST.get('percentage_increase')

        # Lógica MOCK para atualizar o preço na rota
        novo_preco = float(rota.get('km', 0) or 0) * (float(km_value) if km_value else 0)
        novo_preco *= (1 + (float(percentage_increase) if percentage_increase else 0) / 100)
        
        # Simula a atualização do campo R1, R2, etc. na lista MOCK
        rota[round_name] = f"R$ {novo_preco:,.2f} (Manual)"
        
        print(f"Rota {rota_id} | Round {round_name} atualizado. Novo Preço: {rota[round_name]}")
        
        # 🚨 CORREÇÃO: Removido 'cotacao:'
        return redirect('cotacao_bid_detalhe', bid_id=bid_id)

    # Se acessar com GET, redireciona para o detalhe
    # 🚨 CORREÇÃO: Removido 'cotacao:'
    return redirect('cotacao_bid_detalhe', bid_id=bid_id)


# =========================================================================
# NOVA VIEW DE COTAÇÃO EM LOTE
# =========================================================================
def cotacao_round_lote_view(request, bid_id, round_name):
    """ 
    Gerencia a aplicação de uma regra de cálculo em lote para um Round específico
    em todas as rotas do BID.
    """
    
    # 1. Busca as rotas filtradas pelo BID
    rotas_filtradas = get_rotas_for_bid(bid_id)
    
    # Adiciona a função auxiliar ao contexto para ser usada no template
    for rota in rotas_filtradas:
        rota['get_round_price'] = get_round_price(rota, round_name) 
    
    # 🚨 PONTO CHAVE: Defina o contexto ANTES DE QUALQUER REDIRECIONAMENTO ou renderização.
    # O 'bid_id' é crucial para os links de retorno no template.
    context = {
        'bid_id': bid_id,  # <--- Garante que o bid_id está no contexto
        'round_name': round_name,
        'rotas': rotas_filtradas,
        'total_rotas': len(rotas_filtradas)
    }

    if request.method == 'POST':
        # --- APLICAÇÃO EM LOTE ---
        km_value_lote = request.POST.get('km_value_lote')
        percentage_lote = request.POST.get('percentage_increase_lote')
        
        selected_route_ids_str = request.POST.get('selected_route_ids')
        
        # ... (restante da lógica do POST, incluindo a conversão de selected_ids) ...
        
        if not selected_route_ids_str:
            print("ERRO: Nenhuma rota selecionada para aplicação em lote.")
            # Se não houver rotas selecionadas, re-renderiza a página (ou redireciona).
            # Se você re-renderizar, a variável 'context' já está pronta.
            # Se você redirecionar, o problema não acontece aqui. 
            # Vou manter o redirecionamento para o detalhe, que é mais limpo.
            return redirect('cotacao_bid_detalhe', bid_id=bid_id)

        selected_ids = [int(id_str) for id_str in selected_route_ids_str.split(',') if id_str]
        
        if not km_value_lote and not percentage_lote:
            print("ERRO: Nenhum valor de KM ou percentual informado para o lote.")
            # Se houver erro de validação, re-renderiza a página com o contexto atual
            return render(request, 'cotacao_round_lote.html', context)
        else:
            # 2. Loop para aplicar a cotação APENAS nas rotas selecionadas
            for rota in rotas_filtradas:
                if rota['id'] in selected_ids:
                    # ... (Lógica de cálculo) ...
                    pass # Mantido em 'pass' para brevidade
            
            # 3. Redireciona de volta para a tela de detalhes após a aplicação em lote
            return redirect('cotacao_bid_detalhe', bid_id=bid_id)

    # Lógica GET: Apenas renderiza o formulário e a lista de rotas
    return render(request, 'cotacao_round_lote.html', context)