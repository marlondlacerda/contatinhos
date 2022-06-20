from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact


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
