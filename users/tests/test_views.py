from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
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

    def test_login_loads_properly(self):
        """The login page loads properly"""
        # The view function that would be used to serve the URL
        self.assertEquals(resolve('/login/').func.view_class, LoginView)
        path = reverse('login')
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_signup_loads_properly(self):
        """The signup page loads properly"""
        self.assertEquals(resolve('/signup/').func.view_class, SignUpView)
        path = reverse('signup')
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_signup_teamlead_loads_properly(self):
        """The teamlead-signup page loads properly"""
        self.assertEquals(resolve('/signup/teamlead/').func.view_class, BossSignUpView)
        path = reverse('teamlead-signup')
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_signup_employee_loads_properly(self):
        """The employee-signup page loads properly"""
        self.assertEquals(resolve('/signup/employee/').func.view_class, EmployeeSignUpView)
        path = reverse('employee-signup')
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_logout_loads_properly(self):
        """The logout page loads properly"""
        self.assertEquals(resolve('/logout/').func.view_class, LogoutView)
        path = reverse('logout')
        response = self.client.get(path)
        self.assertEquals(response.status_code, 200)

    def test_index_loads_properly(self):
        """The index page loads properly"""
        self.assertEquals(resolve('/').func.view_class, IndexView)
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)


class UrlsWithSlugTestCase(TestCase):
    """Test (boss/slug, project/slug) pages"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='foo', email='foo@user.com', password='123', slug='f-o-o', is_boss=True
        )
        self.boss = Boss.objects.create(user=self.user)
        self.project = Project.objects.create(title='sic egg', slug='sic-egg')

    def test_boss_has_slug(self):
        """Bosses are given slugs correctly when saving"""
        self.assertEquals(resolve('/boss/f-o-o/').func.view_class, BossDetailView)
        path = reverse('users:boss-detail', kwargs={'slug': self.boss.user.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_project_has_slug(self):
        """Projects are given slugs correctly when saving"""
        self.assertEquals(resolve('/project/sic-egg/').func.view_class, ProjectDetailView)
        path = reverse('users:project-detail', kwargs={'slug': self.project.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
