from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.validators import validate_email


def login(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method != "POST":
            return render(request, "accounts/login.html")

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not (username and password):
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, "accounts/login.html")

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.error(request, "Usuário ou senha incorretos.")
            return render(request, "accounts/login.html")

        auth.login(request, user)
        messages.success(request, "Bem Vindo!")
        return redirect("index")


def register(request):
    if request.method != "POST":
        return render(request, "accounts/register.html")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    re_password = request.POST.get("re_password")

    if not (
        first_name
        and last_name
        and username
        and email
        and password
        and re_password
    ):
        messages.error(request, "Por favor, preencha todos os campos.")
        return render(request, "accounts/register.html")

    try:
        validate_email(email)
    except Exception:
        messages.error(request, "Email inválido.")
        return render(request, "accounts/register.html")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Email já cadastrado.")
        return render(request, "accounts/register.html")

    if User.objects.filter(username=username).exists():
        messages.error(request, "Nome de usuário já cadastrado.")
        return render(request, "accounts/register.html")

    if len(password) < 6:
        messages.error(request, "Senha deve ter no mínimo 6 caracteres.")
        return render(request, "accounts/register.html")

    if password != re_password:
        messages.error(request, "Senhas não conferem.")
        return render(request, "accounts/register.html")

    messages.success(request, "Usuário cadastrado com sucesso!")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    user.save()

    return redirect("login")


def logout(request):
    auth.logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect("index")
