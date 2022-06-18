from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from .models import Contact


def index(request):
    contacts = Contact.objects.raw(
        """SELECT *, ROW_NUMBER() OVER(ORDER BY id) as new_id
        FROM agenda.contatos_contact
        WHERE id IN (
            SELECT contact_id FROM agenda.contatos_contacts_user
            WHERE user_id = %s
        )""", [request.user.id]
    )

    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/index.html", {
        "contacts": contacts,
    })


def list_contact(request, contact_id):
    contacts = Contact.objects.raw(
        """SELECT *, ROW_NUMBER() OVER(ORDER BY id) as new_id
        FROM agenda.contatos_contact
        WHERE id IN (
            SELECT contact_id FROM agenda.contatos_contacts_user
            WHERE user_id = %s
        )""", [request.user.id]
    )

    for contact in contacts:
        print(contact.new_id)
        if contact.new_id == contact_id:
            return render(request, "contatos/list_contact.html", {
                "contact": contact,
            })
    else:
        raise Http404("Contact not found")


def search(request):
    term = request.GET.get('q')
    field = Concat('name', Value(' '), 'last_name')

    if term is None or term == "":
        messages.add_message(
            request,
            messages.ERROR,
            "Por favor, digite um termo de busca"
        )
        return redirect("index")

    contacts = Contact.objects.annotate(full_name=field).filter(
        Q(full_name__icontains=term) |
        Q(email__icontains=term) |
        Q(phone__icontains=term)
    )

    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/search.html", {
        "contacts": contacts
    })
