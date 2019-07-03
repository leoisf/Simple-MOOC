#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('simplemooc.courses.views',  # argumetno para não repetição do codigo (prefixo)
    url(r'^$', 'index', name='index'),

    #url(r'^(?P<pk>\d+)/$', 'details', name='details'), # passagen de paramentro para a página com a  chave

    url(r'^(?P<slug>[\w_-]+)/$', 'details', name='details'), # passagen de paramentro para a página com o slug

    url(r'^(?P<slug>[\w_-]+)/inscricao/$', 'enrollment', name='enrollment'), # passagen de paramentro para a página com o slug

    url(r'^(?P<slug>[\w_-]+)/anuncios/$', 'announcements', name='announcements'),# passagen de paramentro para a página com o slug

    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', 'undo_enrollment', name='undo_enrollment'),# passagen de paramentro para a página com o slug
)
