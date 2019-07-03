#-*- coding: utf-8 -*-
from django.template import Library

register = Library()

from simplemooc.courses.models import Enrollment  #importa inscrição

@register.inclusion_tag('courses/templatetags/my_courses.html') #decorater par converter função def my_courses(user): em uma tag
def my_courses(user):
    enrollments = Enrollment.objects.filter(user=user) #filtros para inscrições do usuário
    context = {
        'enrollments': enrollments
    }
    return context #dicionario ocm isncriçõe do usuário

@register.assignment_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)
