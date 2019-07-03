#-*- coding: utf-8 -*-
import re
from django.db import models #implementação do moodel usário seum utilizaro o do django
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin): #herança de metodos já implementados no framework

    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), #validação de caracteres inválidos do nome do usuário
      'O nome de usuário deve conter letras, números ou os caracteres: @/./+/-/_', 'invalid')]
    )

    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False) #verificação do grupo de trabalho
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' #campo unico e referência para o login
    REQUIRED_FIELDS = ['email'] #criação de super usuário

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário' # tratamento para o field label para um ou mais usuários
        verbose_name_plural = 'Usuários'

class PasswordReset(models.Model): #armazenamento da chave única para edição da senha

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário',
    related_name='resets'
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confrimed =models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-created_at']

