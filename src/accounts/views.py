from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .form import RegistrationForm, UserLoginForm
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
            messages.success(request, "Bem vindo de volta!")
            return redirect("contact_list")
        else:
            messages.error(request, "Usuário ou senha inválidos")
            return render(request, "accounts/login.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY
            })


@check_recaptcha
def register(request):
    if request.method != "POST":
        form = RegistrationForm()
        return render(request, "accounts/register.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY
            })

    form = RegistrationForm(request.POST)

    if not form.is_valid():
        erro_display = form.errors.as_data()

        form = RegistrationForm()
        return render(request, "accounts/register.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY,
                'message': erro_display
            })

    form.save()

    messages.success(request, "Usuário criado com sucesso!")
    return redirect("login")


def logout(request):
    auth.logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect("contact_list")
