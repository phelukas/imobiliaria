from django.db import models
from django.conf import settings
from django.utils import timezone


class Cliente(models.Model):

    # Dados
    cpf = models.CharField(unique=True, max_length=13,
                           blank=False, null=False, verbose_name='CPF')
    email = models.EmailField(unique=True, blank=False,
                              null=False, verbose_name='E-mail')
    telefone = models.CharField(
        max_length=15, null=True, blank=True, verbose_name='Telefone')
    primeiro_nome = models.CharField(
        max_length=20, blank=False, null=False, verbose_name='Primeiro nome')
    segundo_nome = models.CharField(
        max_length=20, blank=False, null=False, verbose_name='Segundo nome')

    # Sobre o objeto
    data_cadastro = models.DateTimeField(editable=False)
    data_edicao = models.DateTimeField()
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=True)

    def save(self, *args, **kwargs):

        # Atualizar datas criacao edicao
        if not self.data_cadastro:
            self.data_cadastro = timezone.now()
        self.data_edicao = timezone.now()
        return super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
