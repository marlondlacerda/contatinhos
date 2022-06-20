from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
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


def get_contact_with_new_id(new_id, contacts):
    for contact in contacts:
        if contact.new_id == new_id:
            return contact
    else:
        return None


@login_required(redirect_field_name=None)
def index(request):
    contacts = contact_query_by_user(request.user.id)

    paginator = Paginator(contacts, 8)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, "contatos/contact_list.html", {
        "contacts": contacts,
    })


@login_required(redirect_field_name=None)
def list_contact(request, contact_id):
    contacts = contact_query_by_user(request.user.id)

    contact = get_contact_with_new_id(contact_id, contacts)

    if contact is None:
        raise Http404("Contact not found")
    else:
        return render(request, "contatos/contact_details.html", {
            "contact": contact,
        })


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

    an_object = None
    an_object_string = str(an_object)

    print(an_object_string)

    contacts = contact_query_by_user(request.user.id)

    contacts = [contact for contact in contacts
                if term.casefold() in contact.name.casefold()
                or term.casefold() in str(contact.last_name).casefold()
                or term.casefold()
                in f"{contact.name} {str(contact.last_name)}".casefold()
                or term.casefold() in str(contact.email).casefold()
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
    return redirect("contact_list")


@login_required(redirect_field_name=None)
def edit_contact(request, contact_id):
    contacts = contact_query_by_user(request.user.id)

    contact = get_contact_with_new_id(contact_id, contacts)
    contact = get_object_or_404(Contact, id=contact.id)
    if request.method != "POST":
        form = ContactForm(instance=contact)
        return render(request, "contatos/new_contact.html", {'form': form})

    form = ContactForm(request.POST, request.FILES, instance=contact)

    if not form.is_valid():
        form = ContactForm(instance=contact)
        messages.error(
            request,
            "Número de telefone inválido: Exemplo: (11) 99999-9999",
        )
        return render(request, "contatos/new_contact.html", {'form': form})

    form.save()

    messages.success(request, "Contato editado com sucesso!")
    return redirect("contact_list")
