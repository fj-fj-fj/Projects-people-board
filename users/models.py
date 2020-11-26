from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from autoslug import AutoSlugField


#                   ----------------------------------CustomUser
class User(AbstractUser):
    """auth/login-related fields"""
    # одна модель для аутентификации с возможностью расширения

    is_boss = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username')

    def get_absolute_url(self):
        return reverse('detail_view', kwargs=('slug', self.slug))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

#                   --------------------------------------Leader
class Boss(models.Model):
    """Model representing a leader"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name='юзернэйм'
    )
    project_completed = models.PositiveSmallIntegerField(
        'Успешно завершенные проэкты', blank=True, default=0
    )

    def get_count_succesful_projects(self):
        """Returns number of successfully completed projects"""
        return self.project_completed

    def __str__(self):
        return self.user.username
                
    class Meta:
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководители'


#                   ------------------------------------Employee
class Employee(models.Model):
    """Model representing an employee"""

    # class Level(models.TextChoices):
    #     """TYPE OF USER MAPPING"""
    #     TRAINEE = 'T', _('Thainee')
    #     JUNIOR = 'J', _('Jinior')
    #     MIDDLE = 'M', _('Middle')
    #     SENIOR = 'S', _('Senior')
    # 
    # level = models.CharField(max_length=1, choices=Level.choices, default=Level.TRAINEE)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, verbose_name='юзернэйм'
    )
    leader = models.ForeignKey(
        Boss, blank=True, null=True, on_delete=models.CASCADE, 
        related_name='subordinates', verbose_name='Руководители'
    )
    project = models.ForeignKey(
        'Project', blank=True, null=True, on_delete=models.CASCADE, 
        related_name='employees', verbose_name='Учавствует в проэкте'
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
        related_name='projects', verbose_name='Руководители проэкта'
    )
    
    def get_absolute_url(self, slug):
        return reverse('detail_view', kwargs=('slug', self.slug))
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Проэкт'
        verbose_name_plural = 'Проэкты'





#                   --------------------------------------Signal
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# @receiver(post_save, sender=User)
# def user_type_signal(sender, instance, created, **kwargs):
#     if created:
#         if instance.user_type == 'Leader':
#             Leader.objects.create(profile=instance)
#         else: # == 'Employee':
#             Employee.objects.create(profile=instance)
# 
# https://lincolnloop.com/blog/django-anti-patterns-signals/
