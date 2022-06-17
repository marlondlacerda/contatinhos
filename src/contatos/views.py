from django.shortcuts import render, get_object_or_404
from .models import Contact


def index(request):
    contacts = Contact.objects.all()
    return render(request, "contatos/index.html", {
        "contacts": contacts
    })


def list_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, "contatos/list_contact.html", {
        "contact": contact
    })
