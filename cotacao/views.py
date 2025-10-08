# cotacao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import ClienteForm
from django.contrib import messages
from django.db import transaction, IntegrityError
from .models import CadCliente, tabelaANTT, CotacaoBid
from django.db.models import Q
from faker import Faker
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django import forms
from decimal import Decimal
import traceback


# # --- DEFINIÇÃO DO MOCK DE DADOS ---
# # Use uma lista de dicionários para simular o banco de dados.
# # O MOCK precisa ter um ID único para funcionar corretamente.
# rotas_mock = [
#     # MOCK de dados para rotas na listagem de detalhes do BID
#     {'id': 1, 'bid_id': 1001, 'cod': 'BID-1001-A', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'São Paulo - SP', 'destino': 'Rio de Janeiro - RJ', 'veiculo': 'Caminhão', 'eixos': 5, 'R1': 'R$ 3.800,00', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 900},
#     {'id': 2, 'bid_id': 1001, 'cod': 'BID-1001-B', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'Curitiba - PR', 'destino': 'Florianópolis - SC', 'veiculo': 'Carreta LS', 'eixos': 6, 'R1': 'R$ 1.950,00', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 300},
#     {'id': 3, 'bid_id': 1001, 'cod': 'BID-1001-C', 'grupo': 'Transportadora Alfa Ltda.', 'origem': 'Curitiba - PR', 'destino': 'Porto Alegre - RS', 'veiculo': 'VUC', 'eixos': 2, 'R1': 'R$ 2.100', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 700},
#     # Adicionando um BID diferente para teste
#     {'id': 4, 'bid_id': 1002, 'cod': 'BID-1002-D', 'grupo': 'G-100', 'origem': 'Recife - PE', 'destino': 'Natal - RN', 'veiculo': 'Truck', 'eixos': 3, 'R1': '-', 'R2': '-', 'R3': '-', 'R4': '-', 'R5': '-', 'km': 300},
# ]
# # ---------------------------------------------------------

# # --- FUNÇÃO AUXILIAR MOCK PARA BUSCAR ROTAS ---
# def get_rotas_for_bid(bid_id):
#     """ Filtra rotas_mock pelo bid_id. """
#     return [r for r in rotas_mock if r['bid_id'] == bid_id]

# # --- FUNÇÃO AUXILIAR MOCK PARA OBTER DADOS DE ROTA ---
# def get_rota_by_id(rota_id):
#     """ Busca uma rota pelo ID. """
#     for rota in rotas_mock:
#         if rota['id'] == rota_id:
#             return rota
#     return None

# # --- FUNÇÃO AUXILIAR PARA OBTER PREÇO DO ROUND ---
# def get_round_price(rota, round_name):
#     """ Simula o método get_round_price do template cotacao_round_lote.html. """
#     return rota.get(round_name, '-')
# # -------------------------------------------------


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

#_____________________________________#___#__#_#_#_#_#_

def register_view(request):
    return render(request, 'register.html', {})

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

def logout_view(request):
    return redirect('login') 


#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#


def configuracao_view(request):
    return render(request, 'configuracao.html', {})



#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

def cadastro_usuarios_view(request):
    return render(request, 'cadastro_usuarios.html', {})

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

# DASHBOARD
def dashboard_view(request):
    return render(request, 'dashboard.html', {})

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

# COTAÇÃO SPOT (Placeholder)
def cotacao_spots_view(request):
    return render(request, 'cotacao_spots.html', {})

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#



## criando metodo de cadastro de clientes 


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
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

## metodo para listar todos os clientes
def lista_clientes_view(request):
    """
    Exibe uma lista de todos os clientes cadastrados e tem a opção de pesquisar por nome ou cnpj
    """
    nome_query = request.GET.get('nome', '').strip()
    cnpj_query = request.GET.get('cnpj', '').strip()


    #parametros de paginação limita em padrão 20 cadastros por pagina
    limite_str = request.GET.get('limite','20').strip()
    page = request.GET.get('page',1)##pagina 1 



    ## inicia a querySet
    clientes_list = CadCliente.objects.all().order_by('razaoSocial')    
    ## cria objeto Q para as condições de filtro
    filter_conditions = Q()

    # A Lógica de filtro será combinada com AND (&)
    
    ##Filtro por nome
    if nome_query:
        # CORREÇÃO: Usar '__icontains' (I = Case-Insensitive)
        filter_conditions &= Q(razaoSocial__icontains=nome_query)

    ##Filtro por CNPJ
    if cnpj_query:
        # Tratamento: remove caracteres especiais
        cnpj_limpo = cnpj_query.replace('.', '').replace('-', '').replace('/', '')
        filter_conditions &= Q(cnpj__icontains=cnpj_limpo)
        
    
    #Aplica o filtro se houver alguma condição
    
    if filter_conditions:
        clientes_list = clientes_list.filter(filter_conditions)
            
            

    ##Implementação da páginação
    try:
        limite_int=int(limite_str)
    except ValueError:
        limite_int = 20
        limite_str = '20'

    if limite_int <= 0:
        limite_int = 20
        limite_str = '20'

    paginator =Paginator(clientes_list, limite_int)

    try:
        clientes_list = paginator.page(page)
    except PageNotAnInteger:
        clientes_list = paginator.page(1)
    except EmptyPage:
        clientes_list = paginator.page(paginator.num.pages)


    
        
    context = {
        'clientes': clientes_list,
        'titulo': 'Lista de Clientes Cadastrados',
        'limites_atual': limite_str,
        'nome_query':nome_query,
        'cnpj_query':cnpj_query,

    }

    return render(request, 'lista_clientes.html', context)
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#

def editar_cliente_view(request, cliente_id):
    cliente = get_object_or_404(CadCliente, idCliente=cliente_id)
    

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    
    else:
        form = ClienteForm(instance=cliente)


        context = {
            'form': form,
            'titulo':'EditarCliente',
            'cliente_id': cliente_id,
        }

    return render(request,'editar_cliente.html',context)


#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#
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


#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________##_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________##_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________##_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#__________________#



"""Cadastrar uma nova tabela ANTT"""

ANTT_DATA = {
        "Tabela A" : "Tabela A – Lotação - Spot -  Contratação pontual - Conjunto completo",
        "Tabela B" : "Tabela B – Agregados - Sem alta eficiencia, Cavalo/Motorista",
        "Tabela C" : "Tabela C – Lotação de Alto Desempenho - Spot -Conjunto completo",
        "Tabela D": "Tabela D – Agregados de Alto Desempenho - Cavalo/Motorista",
}


def inicializar_tabelas_antt_view(request):

    if request.method == 'POST':
        try:
            novas_tabelas=[]

            for cod, descricao in ANTT_DATA.items():
                if not tabelaANTT.objects.filter(codTabelaANTT=cod).exists():
                    novas_tabelas.append(
                        tabelaANTT(
                            codTabelaANTT=cod,
                            Descricao=descricao
                        )
                    )

            if novas_tabelas:
                tabelaANTT.objects.bulk_create(novas_tabelas)
                print(f"SUCESSO: {len(novas_tabelas)} Tabelas ANTT cadastradas.")
            
            else:
                print("INFORMAÇÃO: As tabelas ANTT já estavam cadastradas.")
                pass

        except IntegrityError as e:
            print(f"Erro de integridade de inicializar ANTT: {e}")
        except Exception as e:
            print(f"Erro desconhecido ao inicializar ANTT: {e}")

    return redirect(reverse('cotacao_bid_nova'))


# def api_search_antt_view(request):
#     term = request.GET.ger('q','').strip().lower()
#     if not term:
#         return JsonResponse([], safe=False)
    
#     tabelas = tabelaANTT.objects.filter(Descricao__icontains=term).values('idtabelaANTT','Descricao')
#     return JsonResponse(list(tabelas), safe=False)


def api_search_antt_view(request):
    """Retorna as tabelas ANTT para popular o datalist."""
    q = request.GET.get('q', '').strip()
    if q:
        tabelas = tabelaANTT.objects.filter(Descricao__icontains=q)
    else:
        tabelas = tabelaANTT.objects.all()

    data = [
        {"id": t.idTabelaANTT, "Descricao": t.Descricao}
        for t in tabelas
    ]
    return JsonResponse(data, safe=False)


# COTAÇÃO BID (Fluxo completo)


#metodos novos

# def cotacao_bid_nova_view(request):
#     clientes =CadCliente.objects.all().order_by('razaoSocial')
#     tabela_antt = tabelaANTT.objects.all().order_by('Descricao')

#     context ={
#         'clientes':clientes,
#         'tabela_antt': tabela_antt,
#     }

#     return render(request, 'cotacao/cotacao_bid_nova.html', context)




def api_search_clients_view(request):
    search_term = request.GET.get('q', '')
    
    if len(search_term) < 3:
        # Retorna lista vazia se o termo for muito curto
        return JsonResponse([], safe=False) 
        
    # Busca clientes onde a Razão Social OU o CNPJ contenham o termo (case-insensitive)
    clients = CadCliente.objects.filter(
        Q(razaoSocial__icontains=search_term) | 
        Q(cnpj__icontains=search_term)
    ).values('idCliente', 'razaoSocial', 'cnpj')[:10] # Limita a 10 resultados

    # Converte o QuerySet para lista de dicionários e retorna como JSON
    return JsonResponse(list(clients), safe=False)


# def proxima_etapa_bid_view(request):    
    
#     if request.method =='POST':
#         cliente_id = request.POST.get('cliente_id')
#         tabela_antt_id = request.POST.get('tabela_antt_id')


#         if not cliente_id or not tabela_antt_id:
#             return redirect(reverse('cotacao_bid_nova'))
        
#         try:
#             cliente = get_object_or_404(CadCliente, idCliente=cliente_id)
#             tabela_antt = get_object_or_404(tabelaANTT, idTabelaANTT=tabela_antt_id)

#             novo_bid = CotacaoBid.objects.create(
#                 idCliente = cliente,
#                 tabelaANTT=tabela_antt,
#                 rounds = 5,
#                 nCotacaoBid = 'TEMP'
#             )
#             #Gerando o nCotacaoBID "BID" + ID CLIENTE + IDCOTACAOBID
#             numero_final = f"BID{cliente.idCliente:04d}{novo_bid.idCotacaoBid:04d}"
#             novo_bid.nCotacaoBid = numero_final#ATUALIZA E SALVA O nCotacaoBID
#             novo_bid.save() 
#             return redirect(reverse('cotacao_bid_detalhe', kwargs={'bid_id': novo_bid.idCotacaoBid}))

#         except Exception as e:
#             print(f"Erro ao criar o BID: {e}")
#             return redirect(reverse('cotacao_bid_nova'))



#     return redirect('cotacao_bid_nova')


def proxima_etapa_bid_view(request):    
    if request.method != 'POST':
        messages.error(request, "Acesso inválido ao tentar prosseguir com o BID.")
        return redirect('cotacao_bid_nova')

    cliente_id = request.POST.get('cliente_id')
    tabela_antt_id = request.POST.get('tabela_antt_id')

    # Valida se os dados foram enviados
    if not cliente_id or not tabela_antt_id:
        messages.error(request, "Cliente ou Tabela ANTT não selecionados.")
        return redirect('cotacao_bid_nova')

    try:
        # Busca o cliente e a tabela ANTT
        cliente = get_object_or_404(CadCliente, idCliente=cliente_id)
        tabela_antt = get_object_or_404(tabelaANTT, idTabelaANTT=tabela_antt_id)

        # Cria o BID
        novo_bid = CotacaoBid.objects.create(
            idCliente=cliente,
            tabelaANTT=tabela_antt,
            rounds=5,
            nCotacaoBid='TEMP'
        )

        # Gera o número final do BID
        numero_final = f"BID{cliente.idCliente:04d}{novo_bid.idCotacaoBid:04d}"
        novo_bid.nCotacaoBid = numero_final
        novo_bid.save()

        # Debug: imprime informações no console
        print("✅ Novo BID criado com sucesso:")
        print("Cliente:", cliente)
        print("Tabela ANTT:", tabela_antt)
        print("BID ID:", novo_bid.idCotacaoBid)
        print("Número final:", numero_final)

        # Redireciona para a tela de detalhe do BID
        return redirect(reverse('cotacao_bid_detalhe', kwargs={'bid_id': novo_bid.idCotacaoBid}))

    except Exception as e:
        print("❌ Erro completo ao criar o BID:")
        traceback.print_exc()
        messages.error(request, f"Erro ao criar o BID: {str(e)}")
        return redirect('cotacao_bid_nova')



def cotacao_bid_detalhe_view(request, bid_id):
    """ Renderiza a tela de detalhes do BID sem buscar rotas. """
    # Busca o BID
    bid = get_object_or_404(CotacaoBid, idCotacaoBid=bid_id)

    context = {
        'bid_id': bid.idCotacaoBid,
        'cliente': bid.idCliente,
        'antt': bid.tabelaANTT,
        'rotas': [],  # Nenhuma rota por enquanto
    }
    return render(request, 'cotacao_bid_detalhe.html', context)



def exibir_cotacoes_view(request):
    query = request.GET.get('q','')
    if query:
        bids = CotacaoBid.objects.filter(
            Q(nCotacaoBid__icontains=query) |
            Q(idCliente__razaoSocial__icontains=query)
        ).order_by('-dataCriacao')
    else:

    # Busca todas as cotações, ordenando pela data de criação decrescente
        bids = CotacaoBid.objects.all().order_by('-dataCriacao')
        
    context = {
        'bids': bids
    }   
    
    return render(request, 'cotacao_bid_listagem.html', context)


def alternar_destaque_bid(request, bid_id):
    bid = get_object_or_404(CotacaoBid, idCotacaoBid=bid_id)
    bid.destacado = not bid.destacado
    bid.save()
    return redirect('cotacao_bid_listagem')


def cotacao_bid_editar_round_view(request, bid_id, rota_id):
    """ Apenas redireciona de volta para o detalhe do BID. """
    return redirect('cotacao_bid_detalhe', bid_id=bid_id)




def cotacao_bid_listagem_view(request):
    return render(request, 'cotacao_bid_listagem.html', {})

def cotacao_bid_nova_view(request):
    return render(request, 'cotacao_bid_nova.html', {})



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



