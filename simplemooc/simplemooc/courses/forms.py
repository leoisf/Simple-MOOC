#-*- coding: utf-8 -*-
from django import forms
from  django.core.mail import send_mail
from django.conf import settings

from simplemooc.core.mail import send_mail_template

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.CharField(label='E-mail')
    message = forms.CharField(
        label='Mensagem/Dúvida', widget=forms.Textarea
    )

    def send_mail(self, course):
        subject = '[%s] contato ' %course #[%s] forma de formatação de mensagens strings em Python (não nomeada lista)
        # desnecesssario. utilizando o template message = 'Nome: %(name)s; E-mail: %(email)s;%(message)s' # %(name)s forma de formatação de mensagens strings em Python (nomeada dicionartio)
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message']
        }
        template_name = 'courses/contact_email.html'
        send_mail_template(subject, template_name, context, [settings.CONTACT_EMAIL])# envio de e-mail pelo renderizando um template

