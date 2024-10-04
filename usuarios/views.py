from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')


    if senha != confirmar_senha:
        messages.add_message(request, constants.ERROR, 'Senha e confirmar senha estão diferentes')
        return redirect('/usuarios/cadastro/')
    
    if len(senha) < 5:
        messages.add_message(request, constants.WARNING, 'Senha precisa ter mais de 4 caracteres')
        return redirect('/usuarios/cadastro/')
    
    users = User.objects.filter(username=username)

    if users.exists:
        messages.add_message(request, constants.ERROR, 'Já existe um usuario com esse username')
        return redirect('/usuarios/cadastro')
    
    user = User.objects.create_user(username=username, password=senha)

    return redirect('/usuarios/logar/')