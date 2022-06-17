from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .models import Contact


def index(request):
    contacts = Contact.objects.order_by("id").filter(show=True)
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
    print(term)
    if term is None:
        raise Http404("Search term is required")

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
