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

    def test_save(self):
        """Register User object and create Boss object successfully"""
        self.form.save()
        username = User.objects.get(username='foo').__str__()
        self.assertEqual('foo', username)
        boss_object_correctly_saved = Boss.objects.get(user__username=username)
        self.assertEqual('foo', boss_object_correctly_saved.__str__())





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

    def test_save(self):
        """Register User object and create Employee object successfully"""
        self.form.save()
        username = User.objects.get(username='bar').__str__()
        self.assertEqual('bar', username)
        employee_object_correctly_saved = Employee.objects.get(user__username=username)
        self.assertEqual('bar', employee_object_correctly_saved.__str__())


class EmployeeLevelFormTest(TestCase):

    def test_form_inlineformset_factory_field(self):
        """Correct display `level` field"""
        form = EmployeeLevelForm()
        self.assertTrue(list(form.forms[-1].fields.values())[0].label, 'Ваш уровень опыта')
        self.assertFalse(list(form.forms[-1].fields.values())[0].required)
