from django import forms
from django.utils.translation import ugettext_lazy as _
from core.models import Cliente


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ClienteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cliente
        exclude = ('data_edicao','data_cadastro','criado_por',)
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'primeiro_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'cpf': _('CPF'),
            'email': _('E-mail'),
            'primeiro_nome': _('Primeiro nome'),
            'segundo_nome': _('Segundo nome'),
            'telefone': _('Telefone/wpp'),
        }


    def clean(self):
        email = self.cleaned_data.get('email')
        cpf = self.cleaned_data.get('cpf')

        if Cliente.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
            self.add_error('cpf', ' Já existe um perfil vinculado a esse cpf')
        if Cliente.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            self.add_error('email', 'Já existe um perfil vinculado a esse email')
        return self.cleaned_data

    def save(self, commit=True):
        instance = super(ClienteForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance

