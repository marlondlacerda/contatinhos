from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from .models import Contacts_User, Contact


def index(request):
    contacts_user = Contacts_User.objects.filter(user=request.user)

    contacts = Contact.objects.filter(
        show=True,
        id__in=[contact.contact_id for contact in contacts_user]
    )

    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/index.html", {
        "contacts": contacts
    })


def list_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    if not contact.show:
        raise Http404("Contact not found")

    return render(request, "contatos/list_contact.html", {
        "contact": contact
    })


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
