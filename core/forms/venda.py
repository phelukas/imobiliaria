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
        fields = '__all__'

