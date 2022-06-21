from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .form import UserForm, UserLoginForm
from .decorators import check_recaptcha


@check_recaptcha
def login(request):
    if request.user.is_authenticated:
        return redirect("contact_list")
    else:
        if request.method != "POST":
            form = UserLoginForm()
            return render(request, "accounts/login.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY
            })

        form = UserLoginForm(request.POST)

        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            auth.login(request, user)
            return redirect("contact_list")
        else:
            messages.error(request, "Usuário ou senha inválidos")
            return render(request, "accounts/login.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY
            })


def register(request):
    if request.method != "POST":
        return render(request, "accounts/register.html")

    form = UserForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Nome de usuário ou e-mail inválidos.")
        return render(request, "accounts/register.html")

    user = User.objects.create_user(
        first_name=form.cleaned_data.get("first_name"),
        last_name=form.cleaned_data.get("last_name"),
        username=form.cleaned_data.get("username"),
        password=form.cleaned_data.get("password"),
        email=form.cleaned_data.get("email"),
    )
    user.save()

    messages.success(request, "Usuário criado com sucesso!")
    return redirect("login")


def logout(request):
    auth.logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect("contact_list")
