from django.db import models


class Imovel(models.Model):

    # Local
    endereco = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Endereço')
    numero = models.IntegerField(
        blank=False, null=False, verbose_name='Numero')
    bairro = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Bairro')
    complemento = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='Complemento')
    cidade = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='Cidade')
    estado = models.CharField(
        max_length=50, blank=False, null=False, verbose_name='Estado')
    cep = models.CharField(max_length=10, blank=False,
                           null=False, verbose_name='CEP')

    # Valor
    valor = models.DecimalField(max_digits=7, decimal_places=2)

    @property
    def format_endereco(self):
        return '{0}, {1} - {2}'.format(self.endereco, self.numero, self.bairro)
