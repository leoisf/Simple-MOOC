#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm, SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.contrib import messages
from simplemooc.courses.models import Enrollment

from simplemooc.core.mail import send_mail_template
from simplemooc.core.utils import generate_hash_key

from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()

from .forms import RegisterForm, EditAccountForm

@login_required # decoretor em python que executa ao primeiro ao chamar dashboard passa
# que função q verifica se o usuário está logado antes abrir a página caso não esteja faz
# o redirectpafra a pagina de login
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context ={}
    #context['enrollments'] = Enrollment.objects.filter(user=request.user)
    return render(request, template_name, context)

def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'accounts/password_reset.html'
    context ={}
    form = PasswordResetForm(request.POST or None) #modo preechido ou em branco evita repetição do código
    if form.is_valid(): #verifica se o from é em branco ou preenchido
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request,template_name,context)


@login_required()
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user) # model que está sendo alterado com usuário atual
        if form.is_valid():
            form.save()
            messages.success(request,'Dados alterados com sucesso')
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)
