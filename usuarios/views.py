from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants

def cadastrar(request):
    if request.method == "GET":
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')


    if senha != confirmar_senha:
        messages.add_message(request, constants.ERROR, 'Senha e confirmar senha estão diferentes')
        return redirect('usuarios:cadastrar')
    
    if len(senha) < 5:
        messages.add_message(request, constants.WARNING, 'Senha precisa ter mais de 4 caracteres')
        return redirect('usuarios:cadastrar')
    
    users = User.objects.filter(username=username)

    if users.exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuario com esse username')
        return redirect('usuarios:cadastrar')
    
    try:
        user = User.objects.create_user(username=username, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Conta criada com sucesso')
        return redirect('usuarios:login')
    except:
        messages.add_message(request, constants.ERROR, 'Erro na hora da criação tente novamente')
        return redirect('usuarios:cadastrar')



def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('empresas:cadastrar_empresa')
        
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect('usuarios:login')


