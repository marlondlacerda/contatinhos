from django import forms

from contatos.models import Contact


class FormContact(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("show", "created_at")
