from django.db import models
from users.models import User
from core.models.cliente import Cliente
from core.models.imovel import Imovel


FORMA_PAGAMENTO = (
    ("parcelado", "Parcelado em 180"),
    ("avista", " À vista")
)


class Venda(models.Model):

    imovel_imovel = models.OneToOneField(
        Imovel, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='Imóvel', related_name='imovel_vendido')
    valor_imovel = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name='Valor da venda')
    vendedor_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                      blank=False, verbose_name='Vendedor', related_name='vendedor_user')
    cliente_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True,
                                        blank=False, verbose_name='Cliente', related_name='cliente_cliente')
    pagamento = models.CharField(
        max_length=255, choices=FORMA_PAGAMENTO, null=False, blank=False, verbose_name='Forma de pagamento')
    venda_status = models.BooleanField(default=False)
