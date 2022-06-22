from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('O nome é obrigatório.')
        if len(first_name) < 3:
            raise forms.ValidationError(
                'O nome deve ter no mínimo 3 caracteres.'
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('O sobrenome é obrigatório.')
        if len(last_name) < 3:
            raise forms.ValidationError(
                'O sobrenome deve ter no mínimo 3 caracteres.'
            )
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está cadastrado.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError('A senha é obrigatória.')
        if len(password1) < 8:
            raise forms.ValidationError(
                'A senha deve ter no mínimo 8 caracteres.'
            )
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError('Confirme a senha.')
        if password1 != password2:
            raise forms.ValidationError('As senhas não conferem.')

        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=3,
        label='username'
    )
    password = forms.CharField(
        max_length=100,
        min_length=8,
        label='password'
    )
