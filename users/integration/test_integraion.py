import random
import string

from django.urls import reverse
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
        

    def test_querysets_for_the_index_page(self):
        """SELECT * FROM boss INNER JOIN user; SELECT * FROM project"""
        with self.assertNumQueries(2):
            response = self.client.get('/')
        self.assertEqual(response.context['boss_list'].count(), 10)
        self.assertEqual(response.context['project_list'].count(), 5)
        self.assertTemplateUsed(response, 'users/index.html')


    def test_querysets_for_the_projects_detail(self):
        f"""Add 2 bosses and 9 employees to each of 5 projects and
            get 6 queries for each iteration(project): \n{sql}

        """
        def add_employee():
            return self.employees.pop()

        for project in self.projects:
            project.heads.add(*[self.bosses.pop(), self.bosses.pop()])
            project.employees.add(*[add_employee() for _ in range(9)])

        two_bosses_in_project = random.choice(self.projects).heads.count()
        nine_employees_in_project = random.choice(self.projects).employees.count()
        self.assertEqual(two_bosses_in_project, 2)
        self.assertEqual(nine_employees_in_project, 9)
        
        with self.assertNumQueries(30):
            for project in self.projects:
                path = reverse('users:project-detail', kwargs={'slug': project.slug})
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context['boss_list'].count(), 2)
                self.assertEqual(response.context['employee_list'].count(), 9)

        self.assertTemplateUsed(response, 'users/project_detail.html')
        


# наличие 2го SELECT я не понимаю
sql = """
1. SELECT * FROM "project" WHERE "project"."slug" = 'sxy' LIMIT 21
2. SELECT * FROM "project" WHERE UPPER("project"."slug"::text) = UPPER('sxy') LIMIT 21
3. SELECT * FROM "boss" INNER JOIN 
    "project_heads" ON ("boss"."user_id" = "project_heads"."boss_id") WHERE "project_heads"."project_id" = 1
4. SELECT * FROM "user" WHERE "user"."id" IN (81, 91)
5. SELECT * FROM "employee" WHERE "employee"."project_id" = 1
6. SELECT * FROM "user" WHERE "user"."id" IN (96, 97, 98, 99, 100, 92, 93, 94, 95)
"""
