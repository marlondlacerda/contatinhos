from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact, Contacts_User
from .form import ContactForm


def contact_query_by_user(id):
    return Contact.objects.raw(
        """SELECT *, ROW_NUMBER() OVER(ORDER BY name) as new_id
        FROM agenda.contatos_contact
        WHERE id IN (
            SELECT contact_id FROM agenda.contatos_contacts_user
            WHERE user_id = %s
        )""", [id]
    )


@login_required(redirect_field_name=None)
def index(request):
    contacts = contact_query_by_user(request.user.id)

    paginator = Paginator(contacts, 8)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/index.html", {
        "contacts": contacts,
    })


@login_required(redirect_field_name=None)
def list_contact(request, contact_id):
    contacts = contact_query_by_user(request.user.id)

    for contact in contacts:
        if contact.new_id == contact_id:
            return render(request, "contatos/list_contact.html", {
                "contact": contact,
            })
    else:
        raise Http404("Contact not found")


@login_required(redirect_field_name=None)
def search(request):
    term = request.GET.get('q')

    if term is None or term == "":
        messages.add_message(
            request,
            messages.ERROR,
            "Por favor, digite um termo de busca"
        )
        return redirect("index")

    contacts = contact_query_by_user(request.user.id)

    contacts = [contact for contact in contacts
                if term.casefold() in contact.name.casefold()
                or term.casefold() in contact.last_name.casefold()
                or term.casefold()
                in f"{contact.name} {contact.last_name}".casefold()
                or term.casefold() in contact.email.casefold()
                ]

    paginator = Paginator(contacts, 8)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/search.html", {
        "contacts": contacts
    })


@login_required(redirect_field_name=None)
def new_contact(request):
    if request.method != "POST":
        form = ContactForm()
        return render(request, "contatos/new_contact.html", {'form': form})

    form = ContactForm(request.POST, request.FILES)

    if not form.is_valid():
        form = ContactForm()
        messages.error(
            request,
            "Número de telefone inválido: Exemplo: (11) 99999-9999",
        )
        return render(request, "contatos/new_contact.html", {'form': form})

    form.save()

    Contacts_User.objects.create(
        user=request.user,
        contact=Contact.objects.get(id=form.instance.id)
    )

    messages.success(request, "Contato criado com sucesso!")
    return redirect("index")
