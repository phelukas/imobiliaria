from core.models.venda import Venda
from django import forms
from django.utils.translation import ugettext_lazy as _
from core.models import Cliente


class VendaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VendaForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Venda
        exclude = ('vendedor_user', 'valor_imovel', 'venda_status',)

        labels = {
            'imovel_imovel': _('Imovel'),
            'cliente_cliente': _('Cliente'),
            'pagamento': _('Pagamento'),
        }

    def save(self, commit=True):
        instance = super(VendaForm, self).save(commit=False)
        instance.vendedor_user = self.request.user
        x = instance.imovel_imovel.valor
        instance.valor_imovel = instance.imovel_imovel.valor
        if commit:
            instance.save()
        return instance
