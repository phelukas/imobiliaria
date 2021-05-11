from django.forms import widgets
from core.models.venda import Venda
from django import forms
from django.utils.translation import ugettext_lazy as _


class VendaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VendaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Venda
        exclude = ('vendedor_user', 'valor_imovel', 'venda_status',)
        widgets = {
            'imovel_imovel': forms.Select(attrs={'class': 'form-control mt-3'}),
            'cliente_cliente': forms.Select(attrs={'class': 'form-control mt-3'}),
            'pagamento': forms.Select(attrs={'class': 'form-control mt-3'}),
        }
        labels = {
            'imovel_imovel': _('Imovel'),
            'cliente_cliente': _('Cliente'),
            'pagamento': _('Pagamento'),
        }

    def save(self, commit=True):
        instance = super(VendaForm, self).save(commit=False)
        instance.vendedor_user = self.request.user
        instance.valor_imovel = instance.imovel_imovel.valor
        if commit:
            instance.save()
        return instance
