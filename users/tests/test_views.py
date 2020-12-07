from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.views import LoginView, LogoutView

from core.views import (
    SignUpView, BossSignUpView, EmployeeSignUpView
)
from ..views import (
    IndexView, BossDetailView, ProjectDetailView
)
from ..models import Boss, Project


class UrlsTestCase(TestCase):
    """Test (login, signup, signup-teamlead, signup-employee, logout, index) pages"""
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='foo@user.com', password='12test34'
        )

    def tearDown(self):
        self.user.delete()

    def test_login_loads_properly(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(resolve('/login/').func.view_class, LoginView)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='test', password='12test34')
        response = self.client.get(reverse('login'))
        self.assertEqual(str(response.context['user']), 'test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/login.html')

    def test_redirect_if_logged_in(self):
        form_data = {'username': 'test', 'password': '12test34'}
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_signup_loads_properly(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertEqual(resolve('/signup/').func.view_class, SignUpView)
        self.assertContains(response, 
            '<p class="lead">Выберите, какой аккаунт Вы хотите создать</p>', 
            html=True
        )
    
    def test_signup_teamlead_loads_properly(self):
        response = self.client.get(reverse('teamlead-signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')
        self.assertEqual(resolve('/signup/teamlead/').func.view_class, BossSignUpView)

    def test_signup_employee_loads_properly(self):
        response = self.client.get(reverse('employee-signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup_form.html')
        self.assertEqual(resolve('/signup/employee/').func.view_class, EmployeeSignUpView)

    def test_logout_loads_properly(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        self.assertEqual(resolve('/logout/').func.view_class, LogoutView)

    def test_index_loads_properly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        self.assertEqual(resolve('/').func.view_class, IndexView)


class UrlsWithSlugTestCase(TestCase):
    """Test (boss/slug, project/slug) pages"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='foo', email='foo@user.com', password='123', slug='f-o-o', is_boss=True
        )
        self.boss = Boss.objects.create(user=self.user)
        self.project = Project.objects.create(title='sic egg', slug='sic-egg')

    def test_boss_has_slug(self):
        path = reverse('users:boss-detail', kwargs={'slug': self.boss.user.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/boss_detail.html')
        self.assertEqual(resolve('/boss/f-o-o/').func.view_class, BossDetailView)

    def test_project_has_slug(self):
        path = reverse('users:project-detail', kwargs={'slug': self.project.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/project_detail.html')
        self.assertEqual(resolve('/project/sic-egg/').func.view_class, ProjectDetailView)

