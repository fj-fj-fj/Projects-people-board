from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User, Boss, Employee

        
class CrispyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
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

