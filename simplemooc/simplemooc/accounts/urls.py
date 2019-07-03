#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'simplemooc.accounts.views.dashboard', name='dashboard'),  # view para conta do usuário

    url(r'^entrar/$', 'django.contrib.auth.views.login',
    {'template_name': 'accounts/login.html'}, name='login'),  #view para login

    url(r'^cadastre-se/$', 'simplemooc.accounts.views.register',
    name='register'),  #view  para cadastro

    url(r'^sair/$', 'django.contrib.auth.views.logout',
    {'next_page': 'core:home'}, #argumentos nomeados para a função da view
        name='logout'),  #view  para cadastro

    url(r'^editar/$', 'simplemooc.accounts.views.edit',
    name='edit'),  #view  para edição dados do usuário

    url(r'^editar-senha/$', 'simplemooc.accounts.views.edit_password',
    name='edit_password'),  #view  edição de senha

    url(r'^nova-senha/$', 'simplemooc.accounts.views.password_reset',
       name='password_reset'),  # view  para alterar senha

    url(r'^confirmar-nova-senha/(?P<key>\w+)/$', 'simplemooc.accounts.views.password_reset_confirm',
       name='password_reset_confirm'),  # view  para alterar senha
   )

