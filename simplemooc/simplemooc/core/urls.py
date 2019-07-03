#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('simplemooc.core.views', # argumetno para não repetição do codigo (prefixo)
    url(r'^$', 'home', name='home'),
    url(r'^contato/$', 'contact', name='contact'),

)
