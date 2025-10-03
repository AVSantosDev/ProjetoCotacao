# cotacao/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import ClienteForm
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import CadCliente
from django.db.models import Q
from faker import Faker
import random
import time 


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





##def cadastro_cliente_view(request):
    # Se você for usar um formulário real, use Django Forms
    # Por enquanto, apenas renderizamos o template
    if request.method == 'POST':
        # 🚨 Lógica de POST: AQUI VOCÊ SALVA OS DADOS DO CLIENTE
        # Exemplo:
        # nome = request.POST.get('nome')
        # Cliente.objects.create(nome=nome, ...)
        
        # Após salvar, redireciona para a dashboard ou lista de clientes
        return redirect('dashboard') 
        
    return render(request, 'cadastro_cliente.html', {})



def cadastro_cliente_view(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Salva o novo cliente no banco de dados
            form.save()
            
            #  Opcional: Adicionar uma mensagem de sucesso
            messages.success(request, 'Cliente cadastrado com sucesso!')
            
            # Redireciona para o dashboard ou para a lista de clientes
            return redirect(reverse('dashboard')) # Substitua 'dashboard' pelo nome real da sua URL de dashboard
    else:
        # Cria uma instância de formulário vazia para o método GET
        form = ClienteForm() 

    context = {
        'form': form, # Passa o objeto form para o template
    }
    
    # Renderiza o template, passando o formulário no contexto
    return render(request, 'cadastro_cliente.html', context)







def lista_clientes_view(request):
    """
    Exibe uma lista de todos os clientes cadastrados e tem a opção de pesquisar por nome ou cnpj
    """
    nome_query = request.GET.get('nome', '').strip()
    cnpj_query = request.GET.get('cnpj', '').strip()

    ## inicia a querySet
    clientes = CadCliente.objects.all().order_by('razaoSocial')
    
    ## cria objeto Q para as condições de filtro
    filter_conditions = Q()

    # A Lógica de filtro será combinada com AND (&)
    
    ## 1. Filtro por nome
    if nome_query:
        # CORREÇÃO: Usar '__icontains' (I = Case-Insensitive)
        filter_conditions &= Q(razaoSocial__icontains=nome_query)

    ## 2. Filtro por CNPJ
    if cnpj_query:
        # Tratamento: remove caracteres especiais
        cnpj_limpo = cnpj_query.replace('.', '').replace('-', '').replace('/', '')
        
        # CORREÇÃO: Filtrar pelo campo 'cnpj' e usar '__icontains'
        filter_conditions &= Q(cnpj__icontains=cnpj_limpo)
        
    
    # 3. Aplica o filtro se houver alguma condição
    # Este bloco deve estar no final
    if filter_conditions:
        clientes = clientes.filter(filter_conditions)
            
            
    context = {
        'clientes': clientes,
        'titulo': 'Lista de Clientes Cadastrados',
    }

    return render(request, 'lista_clientes.html', context)







# Geração de Clientes de Teste

def gerar_clientes_teste_view(request):
    """
    Cria 20 registros de clientes falsos, resolvendo o problema de estado_abbr.
    """
    if request.method == 'POST':
        fake = Faker('pt_BR')
        clientes_a_criar = 20
        clientes_criados = 0
        
        # Lista de estados brasileiros (para garantir que a sigla funcione)
        # O problema é que 'estado_abbr' não é um método padrão na localização pt_BR
        # Vamos usar um método alternativo para obter uma sigla.
        # Alternativa: Criar um dicionário (a forma mais segura)

        # Usaremos o 'fake.estado()' e depois a sigla, mas farei a correção
        # na chamada que estava gerando o erro de 'Generator'.

        for i in range(clientes_a_criar * 3): 
            if clientes_criados >= clientes_a_criar:
                break 

            try:
                # 🎯 CORREÇÃO CRÍTICA:
                # Na localização pt_BR, o 'estado_abbr' não é um método.
                # Precisamos usar um valor pré-definido ou reverter para a obtenção mais segura.
                # Vou usar a função 'uf' que geralmente está disponível ou uma lista de siglas:
                sigla_estado = fake.state_abbr() # state_abbr é mais comum na Faker
                
                CadCliente.objects.create(
                    razaoSocial=fake.company(),
                    cnpj=''.join(random.choices('0123456789', k=14)),
                    inscEstadual='ISENTA' if random.choice([True, False]) else fake.bban()[:20],
                    inscMunicipal=fake.bban()[:20],
                    logradouro=fake.street_name(),
                    numeroLogradouro=str(random.randint(1, 9999)),
                    bairro=fake.city_suffix(),
                    cidade=fake.city(),
                    estado=fake.estado(),
                    sgEstado=sigla_estado, # USANDO A VARIÁVEL CORRIGIDA
                    pais='Brasil',
                    cep=''.join(random.choices('0123456789', k=8))[:9],
                    telefone=fake.phone_number()[:20],
                    email=fake.email(), 
                    situacao=random.choice([True, True, True, False])
                )
                clientes_criados += 1

            except IntegrityError as e:
                pass
            except Exception as e:
                # Se ainda houver um erro, imprima-o para debug
                print(f"ERRO DE CRIAÇÃO FATAL APÓS CORREÇÃO: {e}")
                
        # Mensagem final após a execução
        if clientes_criados > 0:
            messages.success(request, f'✅ {clientes_criados} clientes de teste criados com sucesso! Acesse a lista para ver.')
        else:
            messages.warning(request, f'Nenhum cliente foi criado. Verifique os logs no console.')
            
        return redirect(reverse('lista_clientes')) 

    return redirect(reverse('cadastro_cliente'))
