from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='Primeiro nome')
    last_name = models.CharField(max_length=20, blank=False, null=False, verbose_name='Segundo nome')
    quantidade_vendas = models.IntegerField(default=0)  
    
    def __str__(self):
        return self.username