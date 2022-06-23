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

        if not form.is_valid():
            erro_display = form.errors.as_data()

            return render(request, "accounts/login.html", {
                "form": form,
                'site_key': settings.RECAPTCHA_PUBLIC_KEY,
                'message': erro_display
            })

        else:
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                auth.login(request, user)
                messages.success(request, "Você foi logado com sucesso!")
                return redirect("contact_list")
            else:
                message = {
                    'invalid_login': 'Usuário ou senha inválidos.'
                }
                messages.error(request, "Usuário ou senha inválidos.")
                return render(request, "accounts/login.html", {
                    "form": form,
                    'site_key': settings.RECAPTCHA_PUBLIC_KEY,
                    'message': message
                })


@check_recaptcha
def register(request):
    if request.user.is_authenticated:
        return redirect("contact_list")

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
