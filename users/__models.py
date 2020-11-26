from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User


class User(models.Model):
    """auth/login-related fields"""

    class Meta:
        abstract = True

    # TYPE_USER = ('L', 'Leader'), ('E', 'Employee')
    # user_type = models.CharField(max_length=1, choices=TYPE_USER)

    def __str__(self):
        return f'[{self.get_type_display()}] {self.username}'


class Boss(User):
    pass


class Employee(User):

    leader = models.ForeignKey(get_user_model(), primary_key=True, on_delete=models.CASCADE)



class Project(models.Models):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    head = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.name




# class Employee(models.Model):
#     name = models.CharField(max_length=50)
#     position = models.CharField(max_length=50)
#     leader = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name


# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)
#     head = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
#     employees = models.ManyToManyField(Employee)

#     def __str__(self):
#         return self.name

# создать работника
# from .models import Book
# e = Employee.objects.create(name='Gosha', position='backend')

# создать проэкт и связать его с руководителем
# from django.contrib.auth import get_user_model
# v = get_user_model().objects.create('vadim')
# p = Project.objects.create(user=v)

# добавлять работников в проэкт
# p.objects.add(e)
# p.objects.all()