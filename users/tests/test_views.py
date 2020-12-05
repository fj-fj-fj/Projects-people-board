from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView, LogoutView

from core.views import (
    SignUpView, BossSignUpView, EmployeeSignUpView
)
from ..views import (
    IndexView, BossDetailView, ProjectDetailView
)
from ..models import Boss, Employee


class UrlsTestCase(TestCase):

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




# NOTE: next: тестировать генерацию слага: boss, project
