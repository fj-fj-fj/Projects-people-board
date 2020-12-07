from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Boss, Employee, Project


class UserTestCase(TestCase):
    """Test user and superuser creation"""
    
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        """Create and save a User successfully"""
        user = self.User.objects.create_user(
            username='foo', email='foo@user.com', password='123'
        )
        self.assertEqual(user.email, 'foo@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='', email='', password='123')

    def test_create_superuser(self):
        """Create and save a SuperUser successfully"""
        admin_user = self.User.objects.create_superuser('root', 'super@user.com', 'toor')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username='gronk', email='super@user.com', password='666', is_superuser=False
            )

    def test_create_boss(self):
        """Create and save a boss successfully"""
        User = get_user_model().objects.create_user(
            username='John Galt', email='boss@user.com', password='1957', is_boss=True
        )
        self.boss = Boss.objects.create(user=User, project_completed=5)
        self.assertIsInstance(self.boss, Boss)
        self.assertNotIsInstance(self.boss, (Employee, Project))

        # user: one2one
        field_label_user = self.boss._meta.get_field('user').verbose_name
        self.assertEqual(field_label_user,'Имя пользователя')

        # subordinates: fk, projects: m2m
        self.assertFalse(self.boss.subordinates.all())
        self.assertFalse(self.boss.projects.all())
        
        # project_completed, get_count_succesful_projects()
        field_label_project_completed = self.boss._meta.get_field('project_completed').verbose_name
        self.assertEqual(field_label_project_completed,'Успешно завершенные проекты')
        self.assertEqual(self.boss.get_count_succesful_projects(), 5)
        self.assertEqual(self.boss.project_completed, 5)

        # __str__
        expected_object_name = self.boss.user.username
        self.assertEqual(expected_object_name, str(self.boss))

        # get_absolute_url()
        self.assertEqual(self.boss.get_absolute_url(), '/boss/john-galt/')
        self.assertNotEqual(self.boss.get_absolute_url(), '/boss/John-Galt/')

        # email
        self.assertEqual(self.boss.user.email, 'boss@user.com')
        self.assertNotEqual(self.boss.user.email, 'morlock@user.com') 

        # is_active, is_boss, not is_employee 
        self.assertTrue(self.boss.user.is_active)
        self.assertTrue(self.boss.user.is_boss)
        self.assertFalse(self.boss.user.is_employee)

    def test_create_employee(self):
        """Create and save an employee successfully"""
        User = get_user_model().objects.create_user(
            username='employee', email='employee@user.com', password='EMPLOYEE', is_employee=True
        )
        self.employee = Employee.objects.create(user=User, level='M')
        self.assertIsInstance(self.employee, Employee)
        self.assertNotIsInstance(self.employee, (Boss, Project))

        # user: one2one
        field_user_label = self.employee._meta.get_field('user').verbose_name
        self.assertEqual(field_user_label,'Имя пользователя')

        # leader: fk
        field_leader = self.employee._meta.get_field('leader').verbose_name
        self.assertEqual(field_leader,'Руководители')
        self.assertIsNone(self.employee.leader)

        # project: fk
        field_project = self.employee._meta.get_field('project').verbose_name
        self.assertEqual(field_project,'Учавствует в проекте')
        self.assertIsNone(self.employee.project)

        # level (selected: middle)
        max_length = self.employee._meta.get_field('level').max_length
        self.assertEqual(max_length, 1)
        self.assertMultiLineEqual(self.employee.level, 'M')
        self.assertEqual(self.employee.get_position(), 'M')

        # __str__
        expected_object_name = self.employee.user.username
        self.assertEqual(expected_object_name, str(self.employee))

        # email
        self.assertEqual(self.employee.user.email, 'employee@user.com')
        self.assertNotEqual(self.employee.user.email, 'eloi@user.com')

        # is_active, is_employee, not is_boss
        self.assertTrue(self.employee.user.is_active)
        self.assertTrue(self.employee.user.is_employee)
        self.assertFalse(self.employee.user.is_boss)

    def test_create_project(self):
        """Create and save a project successfully"""
        project = Project.objects.create(title='Agony soft')
        self.assertIsInstance(project, Project)
        self.assertNotIsInstance(project, (Boss, Employee))
        
        # heads: m2m
        field_heads = project._meta.get_field('heads').verbose_name
        self.assertEqual(field_heads, 'Руководители проекта')
        self.assertFalse(project.heads.all())

        # employees: fk
        self.assertFalse(project.employees.all())

        # __str__
        expected_object_name = project.title
        self.assertEqual(expected_object_name, str(project))

        # title, description
        self.assertEqual(project.title, 'Agony soft')
        self.assertEqual(project.description, '')

        # get_absolute_url()
        self.assertEqual(project.get_absolute_url(), '/project/agony-soft/')
        self.assertNotEqual(project.get_absolute_url(), '/project/Agony soft/')
