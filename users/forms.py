""" This module contains forms for registration of 
        two types of user `employee` and `boss`. 
    
    It also contains crispy (CrispyUserCreationForm):
    https://django-crispy-forms.readthedocs.io/en/latest/

"""
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User, Boss, Employee


EmployeeLevelForm = inlineformset_factory(
    User, Employee, fields=('level',)
)

        
class CrispyUserCreationForm(UserCreationForm):
    """General model and fields form both types of user"""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """Crispy: set up some basic `FormHelper` attributes"""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class BossSignUpForm(CrispyUserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_boss = True
        if commit:
            user.save()
            Boss.objects.create(user=user)
        return user


class EmployeeSignUpForm(CrispyUserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True
        if commit:
            user.save()
            Employee.objects.create(user=user)
        return user

