from django.shortcuts import render, redirect
from empresarios.models import Empresas, Documento, Metricas
from .models import PropostaInvestimento
from django.contrib.messages import constants
from django.contrib import messages
from django.http import Http404


def sugestao(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    
    areas = Empresas.area_choices

    if request.method == "GET":
        return render(request, 'sugestao.html', {'areas': areas})
    elif request.method == "POST":
        tipo = request.POST.get('tipo')
        area = request.POST.getlist('area')
        valor = request.POST.get('valor')

        if tipo == 'C':
            empresas = Empresas.objects.filter(tempo_existencia='+5').filter(estagio='E')
        elif tipo == 'D':
            empresas = Empresas.objects.filter(tempo_existencia__in=['-6', '+6', '+1']).exclude(estagio='E')
        elif tipo == 'T':
            empresas = Empresas.objects.all()


        empresas = empresas.filter(area__in=area)

        empresas_selecionadas = []

        for empresa in empresas:
            percentual = float(valor) * 100 / float(empresa.valuation)
            if percentual >= 1:
                empresas_selecionadas.append(empresa)
    
    return render(request, 'sugestao.html', {'areas': areas, 'empresas': empresas_selecionadas})


def ver_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    documentos = Documento.objects.filter(empresa=empresa)

    metricas = Metricas.objects.filter(empresa=empresa)
    return render(request, 'ver_empresa.html', {'empresa': empresa, 'documentos': documentos, 'metricas': metricas})



def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresas.objects.get(id=id)

    propostas_aceitas = PropostaInvestimento.objects.filter(empresa=empresa).filter(status='PA')


    if not valor.strip() or not percentual.strip() or valor.strip() == '0' or percentual.strip() == '0':
        messages.add_message(request, constants.ERROR, 'Os campos valor e investimentos não podem ficar vazios e nem valores abaixo de 1')
        return redirect('investidores:ver_empresa', id)


    total = 0

    for pa in propostas_aceitas:
        total = total + pa.percentual

    try:
        if total + int(percentual) > empresa.percentual_equity:
            messages.add_message(request, constants.WARNING, 'O percentual solicitado ultrapassa o percentual máximo')
            return redirect('investidores:ver_empresa', id)
    except ValueError:
        messages.add_message(request, constants.ERROR, 'Erro tente novamente')
        return redirect('investidores:ver_empresa', id)
    

    valuation = (100 * int(valor)) / int(percentual)

    if valuation < (int(empresa.valuation / 2)):
        messages.add_message(request, constants.WARNING, f'Seu valuation proposto foi de R${valuation:.2f}, e deve ser o mínimo R${empresa.valuation:.2f}')
        return redirect('investidores:ver_empresa', id)

    try:
        propostas_investimentos = PropostaInvestimento(
            valor=valor,
            percentual=percentual,
            empresa=empresa,
            investidor=request.user
        )

        propostas_investimentos.save()
        messages.add_message(request, constants.SUCCESS, 'Proposta enviada com sucesso')
        return redirect('investidores:assinar_contrato', propostas_investimentos.id)
    except:
        messages.add_message(request, constants.ERROR, 'Erro no envio de proposta tente novamente')
        return redirect('investidores:assinar_contrato', propostas_investimentos.id)

def assinar_contrato(request, id):
    propostas_investimentos = PropostaInvestimento.objects.get(id=id)
    
    if propostas_investimentos.status != 'AS':
        raise Http404()
    
    if request.method == 'GET':
        return render(request, 'assinar_contrato.html', {'propostas_investimentos': propostas_investimentos})

    elif request.method == 'POST':
        selfie = request.FILES.get('selfie')
        rg = request.FILES.get('rg')

        propostas_investimentos.selfie = selfie
        propostas_investimentos.rg = rg
        propostas_investimentos.status = 'PE'
        propostas_investimentos.save()
        messages.add_message(request, constants.SUCCESS, 'Contrato assinado com sucesso, sua proposta foi enviada')
        return redirect('investidores:ver_empresa', propostas_investimentos.empresa.id)
        
