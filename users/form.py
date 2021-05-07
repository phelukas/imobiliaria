from django import forms
from django.contrib.auth import authenticate
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class':'fadeIn second', 'placeholder':'username'}),
            'password': forms.PasswordInput(attrs={'class':'fadeIn third', 'placeholder':'password'})
        }


    # Validar/autenticar campos de login
    def clean(self):
        username = self.cleaned_data.get('username')
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


