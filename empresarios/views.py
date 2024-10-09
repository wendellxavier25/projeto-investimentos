from django.shortcuts import render, redirect
from .models import Empresas
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
    