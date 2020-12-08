from django.test import TestCase
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model

from ..models import User, Boss, Employee

from ..forms import (
    BossSignUpForm, EmployeeSignUpForm, EmployeeLevelForm
)


class BossSignUpFormTest(TestCase):
    
    def setUp(self):
        new_boss = {
            'username': 'foo', 
            'email': 'foo@gmail.com', 
            'password1': '0x05175510', 
            'password2': '0x05175510'
        }
        self.form = BossSignUpForm(new_boss)

    def test_form_data_is_valid(self):
        """Check form.is_valid()"""
        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.cleaned_data)
        form = BossSignUpForm({})
        self.assertTrue(form.errors)


class EmployeeSignUpFormTest(TestCase):

    def setUp(self):
        new_employee = {
            'username': 'bar', 
            'email': 'bar@gmail.com', 
            'password1': '0x05175511', 
            'password2': '0x05175511',
        }
        self.form = EmployeeSignUpForm(new_employee)

    def test_form_data_is_valid(self):
        """Check form.is_valid()"""
        self.assertTrue(self.form.is_valid())
        self.assertTrue(self.form.cleaned_data)
        form = EmployeeSignUpForm({})
        self.assertTrue(form.errors)


class EmployeeLevelFormTest(TestCase):

    def test_form_inlineformset_factory_field(self):
        """Correct display `level` field"""
        form = EmployeeLevelForm()
        self.assertTrue(list(form.forms[-1].fields.values())[0].label, 'Ваш уровень опыта')
        self.assertFalse(list(form.forms[-1].fields.values())[0].required)
