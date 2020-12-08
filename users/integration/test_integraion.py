import random
import string

from django.test import TestCase, tag
from django.contrib.auth import get_user_model

from ..models import User, Boss, Employee, Project


@tag('slow')
class IntegraionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create 5 projects and 100 users: 10 bosses, 90 employees"""
        cls.bosses = []
        cls.employees = []
        cls.projects = []

        def create_new_user():
            username = ''.join(random.sample(string.ascii_lowercase, 8))
            email = username + '@django.com'
            password = username[::-1]
            user = User.objects.create_user(**locals())
            return user

        for i in range(100):
            user = create_new_user()
            if i % 10 == 0:
                boss = Boss.objects.create(user=user)
                boss.user.is_boss = True
                cls.bosses.append(boss)
            else:
                employee = Employee.objects.create(user=user)
                employee.user.is_employee = True
                cls.employees.append(employee)

        for i in range(5):
            title = ''.join(random.sample(string.ascii_lowercase, 3))
            project = Project.objects.create(title=title)
            cls.projects.append(project)
        

    def test_add_people_to_projects(self):
        """Add 2 bosses and 9 employees to each project"""
        
        def self_employees_pop():
            return self.employees.pop()

        for project in self.projects:
            project.heads.add(*[self.bosses.pop(), self.bosses.pop()])
            project.employees.add(*[self_employees_pop() for _ in range(9)])


# ----------------------------------------------------------------------
# Ran 1 test in 20.083s

# OK

# NOTE: тест показал сломанное отношение m2m 
# through удалено
# on_delete.CASCADE пересмотреть