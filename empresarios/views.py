from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresas, Documento, Metricas
from investidores.models import PropostaInvestimento
from django.contrib.messages import constants
from django.contrib import messages




def cadastrar_empresa(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')

    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html',
                       {'tempo_existencias': Empresas.tempo_existencia_choices,
                        'areas': Empresas.area_choices,})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final_captacao = request.POST.get('data_final_captacao')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        if not cnpj or len(cnpj.strip()) != 14 or cnpj.isdigit():
            messages.add_message(request, constants.ERROR, 'CNPJ contem 12 dígitos')
            return redirect('empresas:cadastrar_empresa')

        if not all([nome, cnpj, site, tempo_existencia, descricao, data_final_captacao, percentual_equity, estagio, area, publico_alvo, valor]):
            messages.add_message(request, constants.ERROR, 'Todos os campos são obrigatórios.')
            return redirect('empresas:cadastrar_empresa')
        
        if pitch is None and logo is None:
            messages.add_message(request, constants.ERROR, 'Campos de pitch e logo são obrigatórios')
            return redirect('empresas:cadastrar_empresa')
        
        if Empresas.objects.filter(site=site).exists():
            messages.add_message(request, constants.ERROR, 'Esse site já está cadastrado no banco de dados')
            return redirect('empresas:cadastrar_empresa')

        if Empresas.objects.filter(nome=nome).exists():
            messages.add_message(request, constants.ERROR, 'Nome de empresa já existente')
            return redirect('empresas:cadastrar_empresa')

        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final_captacao,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
        except:
            messages.add_message(request, constants.ERROR, 'Erro no cadastros de dados, tente novamente')
            return redirect('empresas:cadastrar_empresa')

        empresa.save()
        messages.add_message(request, constants.SUCCESS, 'Dados salvos com sucesso')
        return redirect('empresas:cadastrar_empresa')
    

def listar_empresas(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    
    if request.method == "GET":

        nome_empresa = request.GET.get('empresa')

        empresas = Empresas.objects.filter(user=request.user)

        if nome_empresa:
            empresas = empresas.filter(nome__icontains=nome_empresa)

        return render(request, 'listar_empresas.html', {'empresas': empresas, 'nome_empresa': nome_empresa })
    

def empresa(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    empresa = Empresas.objects.get(id=id)

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não é sua')
        return redirect('empresas:listar_empresas')


    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        propostas_investimentos = PropostaInvestimento.objects.filter(empresa=empresa)
        
        percentual_vendido = 0
        

        for pi in propostas_investimentos:
            if pi.status == 'PA':
                percentual_vendido += pi.percentual
                

        total_captado =  sum(propostas_investimentos.filter(status='PA').values_list('valor', flat=True))

        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0

        propostas_investimentos_enviada = propostas_investimentos.filter(status='PE')

        return render(request, 'empresa.html', {'empresa': empresa, 'documentos': documentos, 'propostas_investimentos_enviada': propostas_investimentos_enviada, 'percentual_vendido': int(percentual_vendido),
                                                 'total_captado': total_captado, 'valuation_atual': valuation_atual})
    

def add_doc(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa empresa não é sua')
        return redirect('empresas:listar_empresas')

    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, 'Envie um arquivo em PDF')
        return redirect('empresas:empresa', id)

    if not arquivo:
        messages.add_message(request, constants.ERROR, 'Envie um arquivo')
        return redirect('empresas:empresa', id)

    documento = Documento(empresa=empresa, titulo=titulo, arquivo=arquivo)
    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Arquivos salvos com sucesso')
    return redirect('empresas:empresa', id)


def excluir_dc(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    documento = get_object_or_404(Documento, id=id)

    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR, 'Esse documento não é seu')
        return redirect('empresas:listar_empresas')
    
    documento.delete()
    messages.add_message(request, constants.SUCCESS, 'Documento deletado com sucesso')
    return redirect('empresas:empresa', documento.empresa.id)


def add_metrica(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get("titulo")
    valor = request.POST.get("valor")

    metrica = Metricas(empresa=empresa, titulo=titulo, valor=valor)
    metrica.save()

    messages.add_message(request, constants.SUCCESS, 'Metrica cadastrada com sucesso')
    return redirect('empresas:empresa', empresa.id)



def gerenciar_proposta(request, id):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    acao = request.GET.get('acao')
    pi = PropostaInvestimento.objects.get(id=id)
    

    if acao == 'aceitar':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita')
        pi.status = 'PA'

    elif acao == 'negar':
        messages.add_message(request, constants.SUCCESS, 'Proposta negada')
        pi.status = 'PR'

    pi.save()
    return redirect('empresas:empresa', pi.empresa.id)