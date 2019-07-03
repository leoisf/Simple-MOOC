#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key

from .models import PasswordReset

User = get_user_model()

class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self): #retorna o valor a ser pegadno pelo form
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): #verifica se existe o usuário cadastrado no sistema
            return email
        raise forms.ValidationError(
            'Usuário não encontrado'
        )

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.name)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'accounts/password_reset_mail.html'
        subject = 'Resetar senha no Simple Mooc'
        context = {
            'reset': reset
        }
        send_mail_template(subject, template_name, context, [user.email] )




class RegisterForm(forms.ModelForm):

    #email = forms.EmailField(label='E-mail') em fields

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Senhas diferentes')
        return password2

    # def clean_email(self):
    #     email = self.cleaned_data['email'] # pega o valor do campo e-mail submetido pelo usuário
    #     if User.objects.filter(email=email).exists(): # busca e-mail no banco ( retorna bool)
    #         raise forms.ValidationError('Já existe Usuário cadastrado com este E-mail') # lança uma exceção
    #     return email # retorna valor fornecido pelo usuário

    def save(self, commit=True): #sobrescrita do metodo save que substituido de UserCreationForm
        user = super(RegisterForm, self).save(commit=False) #retorna os dados sem salvar o usuário
        #user.email = self.cleaned_data['email'] # valores do form já validados
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save() #salva usuário com e-mail
        return user

    class Meta:
        model = User
        fields = ['username', 'email']



class EditAccountForm(forms.ModelForm): #formulário para um modelo que gera campos especificos de acordo com um model

    # def clean_email(self):
    #     email = self.cleaned_data['email'] # pega o valor do campo e-mail submetido pelo usuário
    #     queryset = User.objects.filter(email = email).exclude(pk=self.instance.pk) #exclude filter con um not - menos o email enm questão
    #     if queryset: #busca e-mail no banco (retorna bool)
    #         raise forms.ValidationError('Já existe Usuário cadastrado com este E-mail') # lança uma exceção
    #     return email # retorna valor fornecido pelo usuário

    class Meta:
        model = User
        fields = ['username', 'email', 'name'] #campos que pode ser alterados


