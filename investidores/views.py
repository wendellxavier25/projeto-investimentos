from django.shortcuts import render, redirect
from empresarios.models import Empresas, Documento, Metricas
from .models import PropostaInvestimento
from django.contrib.messages import constants
from django.contrib import messages


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
        messages.add_message(request, constants.ERROR, 'Os campos valor e investimentos não podem ficar vazios')
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


    proposta_investimento = PropostaInvestimento(
        valor=valor,
        percentual=percentual,
        empresa=empresa,
        investidor=request.user
    )

    proposta_investimento.save()
    return redirect('investidores:assinar_contrato', proposta_investimento.id)