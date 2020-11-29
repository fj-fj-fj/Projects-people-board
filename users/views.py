from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from users.models import User, Boss, Project


class IndexView(ListView):
    model = Boss
    template_name = 'users/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['boss_list'] = Boss.objects.all()
        context['project_list'] = Project.objects.all()
        return context


class BossDetailView(DetailView):
    model = Boss
    template_name = 'users/boss_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        user = User.objects.get(slug__iexact=slug)
        boss = Boss.objects.get(user=user)
        return boss

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context.update({
            'boss': self.object,
            'project_list': self.object.projects.all(),
            'employee_list': self.object.subordinates.all(),
        })
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'users/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        
        project = get_object_or_404(Project, slug__iexact=self.kwargs['slug'])

        context.update({
            'project': project,
            'boss_list': project.heads.all(),
            'employee_list': project.employees.all()
        })
        return context

