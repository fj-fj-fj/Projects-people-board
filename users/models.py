from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse

from autoslug import AutoSlugField


#                   ----------------------------------CustomUser
class User(AbstractUser):
    """auth/login-related fields"""

    is_boss = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

#                   --------------------------------------Leader
class Boss(models.Model):
    """Model representing a leader"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name='Имя пользователя'
    )
    project_completed = models.PositiveSmallIntegerField(
        'Успешно завершенные проекты', blank=True, default=0
    )

    def get_count_succesful_projects(self):
        """Returns number of successfully completed projects"""
        return self.project_completed

    def get_absolute_url(self):
        return reverse('users:boss_detail_url', kwargs=('slug', self.slug))

    def __str__(self):
        return self.user.username
                
    class Meta:
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководители'


#                   ------------------------------------Employee
class Employee(models.Model):
    """Model representing an employee"""

    class Level(models.TextChoices):
        """TYPE OF USER MAPPING"""
        TRAINEE = 'T', _('Thainee')
        JUNIOR = 'J', _('Jinior')
        MIDDLE = 'M', _('Middle')
        SENIOR = 'S', _('Senior')
    
    level = models.CharField(max_length=1, choices=Level.choices, default=Level.TRAINEE)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name='Имя пользователя'
    )
    leader = models.ForeignKey(
        Boss, blank=True, null=True, on_delete=models.CASCADE, 
        related_name='subordinates', verbose_name='Руководители'
    )
    project = models.ForeignKey(
        'Project', blank=True, null=True, on_delete=models.CASCADE, 
        related_name='employees', verbose_name='Учавствует в проекте'
    )

    def get_position(self):
        """Returns employee position (trainee, junior, middle or senior)"""
        return self.level

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


#                   -------------------------------------Project
class Project(models.Model):
    """Model representing a project"""

    title = models.CharField('Название', max_length=100, db_index=True)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField('Описание', blank=True)
    heads = models.ManyToManyField(
        Boss, blank=True, through=Employee, 
        related_name='projects', verbose_name='Руководители проекта'
    )
    
    def get_absolute_url(self, slug):
        return reverse('users:project_detail_url', kwargs=('slug', self.slug))
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
