from django import forms

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    re_password = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário Já existe')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Já existe')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError(
                'Senha deve ter no mínimo 6 caracteres')
        if password != self.cleaned_data['re_password']:
            raise forms.ValidationError(
                'Senhas não conferem')
        return password


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='username'
    )
    password = forms.CharField(
        max_length=100,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='password'
    )
