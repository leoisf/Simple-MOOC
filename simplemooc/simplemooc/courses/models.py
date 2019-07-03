# -*- coding: utf-8 -*-
from django.db import models

from simplemooc import settings

# Create your models here.

class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )


class Course(models.Model):
    name = models.CharField('Nome', max_length=100) # Nome -> verbose name para field do form
    slug = models.SlugField('Atalho')  # atalhos para urls mais informativas
    description = models.TextField('Descricação', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    start_date = models.DateField('Data de Inicio', null=True, blank=True)
    image = models.ImageField(upload_to='courses/images', verbose_name='Imagem',
                              null=True, blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)  # data atual automática criação
    update_at = models.DateTimeField('Atualizado em', auto_now=True)  # data atual automática  atualização

    objects = CourseManager()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('courses:details', (), {'slug': self.slug}) #utilização do atalho para chamada da págia ao inves do id do curso.

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering=['name']

class Enrollment(models.Model): #model para inscrição

    STATUS_CHOICES = ( #tupla de tupla para o status da inscrição
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='enrollments'
    )

    course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollments')
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=1, blank=True)

    created_at = models.DateTimeField('criado em', auto_now_add=True)  # data atual automática criação
    update_at = models.DateTimeField('Atualizado em', auto_now=True)  # data atual automática  atualização

    def active(self):
        self.status = 1 #indica a inscrição do aluno
        self.save()

    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'), ) # index indice de unicidade (uma inscrição para usuário e curso)


