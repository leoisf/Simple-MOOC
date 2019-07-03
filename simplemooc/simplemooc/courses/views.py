#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required #força login do usuário
from django.contrib import messages

from .models import Course, Enrollment #import do models a serem listados
from .forms import ContactCourse # formulário contato para a pagina de cursos

# Create your views here.

def index(request):
    courses = Course.objects.all() # model.manage.objetos
    template_name = 'courses/index.html'
    context = {
        'courses': courses #lista de cursos all
    }
    return render(request, template_name, context) # contexto (dicionário) variáveis que substituirão valores na página

# def details(request, pk):
#     course = get_object_or_404(Course, pk=pk) chamada da página cursos com a chave
#     context ={
#         'course': course
#     }
#     template_name = 'courses/details.html'
#     return render(request,template_name, context)
def details(request, slug):
    course = get_object_or_404(Course, slug=slug) #  chamada da página cursos com o slug (atalho)
    context ={}
    if request.method == 'POST':
        form = ContactCourse(request.POST) # post - dicionário com todos os valores dos campos do formulário
        if form.is_valid(): #validação dos campos
            context['is_valid'] = True
            form.send_mail(course)
            print(form.cleaned_data) #impressão dos dados no console
            form = ContactCourse()
    else:
        form = ContactCourse() #formulário em branco
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request,template_name, context)

@login_required #requer que o usuário esteja logado
def enrollment(request, slug):  #inscrição
    course = get_object_or_404(Course, slug=slug) #verifica a inscrição do usuário atravez do slug
    erollment, created = Enrollment.objects.get_or_create(user=request.user, #retorna tupla inscriçãeo e bool que diz se criado
        course=course
    )#recebe um filtro e para listar usuario atual e curso em questão
    if created:
        #     enrollment.active()
        messages.success(request, 'Inscrição realizada com sucesso!')
    else:
        messages.info(request, 'Você já está instrito neste curso')
    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template, context)

@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)  #verifica a inscrição do usuário
    if not request.user.is_staff: #verifica previlégios do usuário
        enrollment = get_object_or_404(
            Enrollment, user=request.user, course=course )# retorna tupla inscriçãeo e bool que diz se criado
        if not enrollment.is_approved():
            messages.error(request, 'Inscrição pendente')
            return redirect('accounts:dashboard')
    template = 'courses/announcements.html'
    context = {
        'course': course
    }
    return render(request, template, context)

