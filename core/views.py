from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, TemplateView
)
from users import forms
from users.models import User, Employee


class SignUpView(TemplateView):
    """pre-signup with user type selection"""

    template_name = 'registration/signup.html'


class BossSignUpView(CreateView):
    """Registration of user type `boss`"""

    model = User
    form_class = forms.BossSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'boss'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:index_url')


# Для добавления поля из связанной модели, модифицировал вью

class EmployeeSignUpView(CreateView):
    """Registration of user type `employee` with 
        additional field `level` of experience 

        will show also:
        <select>
            trainee(default), junior, middle, senior
        </select>
    """

    model = User
    form_class = forms.EmployeeSignUpForm
    template_name = 'registration/signup_form.html'

    def get(self, request, *args, **kwargs):

        # Я использую `inlineformset_factory` и добавляю поле `level` из `model.Employee`
        # К полям [username, email, password1, password2] будет добавлен `level`

        self.object = None 
        form_class = self.get_form_class()
        
        form = self.get_form(form_class)
        employee_level = forms.EmployeeLevelForm()  #

        return self.render_to_response(
            self.get_context_data(
                form=form, employee_level=employee_level
            )
        )
    
    def post(self, request, *args, **kwargs):

        self.object = None
        form = self.get_form()
        employee_level = forms.EmployeeLevelForm(request.POST)  #

        if form.is_valid() and employee_level.is_valid():

            # FIXME: Я запутался, пусть временно будет вот эта херня:

            level = dict(request.POST).get('employee-0-level', 'T')
            self.object = form.save()
            e = Employee.objects.get(user=self.object)
            e.level = level[0]
            e.save()
            # print(0, form.instance.employee.user) # entered username, ok
            # print(1, form.instance.employee.level) # It's still default
            
            login(self.request, self.object)

            return redirect('users:index_url')
        return self.form_invalid(form, employee_level)
    

    def form_invalid(self, form, employee_level):
        return self.render_to_response(
            self.get_context_data(form=form, employee_level=employee_level)
        )

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)



# class DampSquib:
#     AttributeError: 'TypedChoiceField' object has no attribute 'values'
#     AttributeError: 'EmployeeSignUpView' object has no attribute 'object'
#     ValueError: save() prohibited to prevent data loss due to unsaved related object 'user'.
#     users.models.User.employee.RelatedObjectDoesNotExist: User has no employee.
#     users.models.Employee.DoesNotExist: Employee matching query does not exist.
#     AttributeError: Generic detail view EmployeeSignUpView must be called with either an object pk or a slug in the URLconf.
#     etc
