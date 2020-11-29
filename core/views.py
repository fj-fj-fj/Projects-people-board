from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from users.models import User
from users.forms import BossSignUpForm
from users.forms import EmployeeSignUpForm
from users.forms import EmployeeLevelForm


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class BossSignUpView(CreateView):
    model = User
    form_class = BossSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'boss'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:index_url')


class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:index_url')
