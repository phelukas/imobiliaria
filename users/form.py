from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
        }

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"E-mail ou senha inválidos.")
        return self.cleaned_data

    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"E-mail ou senha inválidos.")
        return user


class CriarUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': 'Senha'}), label='Senha')
    confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control line-input', 'placeholder': 'Confirme a senha'}), label='Confirme sua senha')
    email = forms.CharField(widget=forms.EmailInput(attrs={
                            'class': 'form-control line-input', 'placeholder': 'Ex.: pedro@gmail.com'}), label='email')
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control line-input', 'placeholder': 'Ex.: Pedro'}), label='Primeiro nome')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control line-input', 'placeholder': 'Ex.: Silva'}), label='Ultimo nome')

    class Meta:
        model = User
        exclude = ('quantidade_vendas',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        if password != confirm:
            self.add_error('password', 'São não são iguais')
        return super().clean()

    def save(self, commit=True):
        user = super(CriarUserForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
