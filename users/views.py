from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from users.models import Boss, Project


class IndexView(ListView):
    model = Boss
    template_name = 'users/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boss_list'] = self.model.objects.select_related("user").all()
        context['project_list'] = Project.objects.all()
        return context


class BossDetailView(DetailView):
    model = Boss
    template_name = 'users/boss_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        return self.model.objects.select_related('user') \
                   .get(user__slug__iexact=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'boss': self.object,
            'project_list': self.object.projects.all(),
            'employee_list': self.object.subordinates \
                                 .prefetch_related('user').all()
        })
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'users/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        project = get_object_or_404(self.model, slug__iexact=slug)
        context.update({
            'project': project,
            'boss_list': project.heads.prefetch_related('user').all(),
            'employee_list': project.employees.prefetch_related('user').all()
        })
        return context




# NOTE: About the difference in the number of db queries
#
# Boss.objects.all()  # len(connection.queries) - 9
# ✔️ Boss.objects.select_related("user").all() # 1
#
# Project.objects.all()  # 1
#
# Boss.subordinates.all()  # 9
# ✔️ Boss.subordinates.prefetch_related('user').all()  # 3
#
# project = Project.objects.get(slug__iexact=slug)  # 1
#
# project.heads.all() # 3
# ✔️ project.heads.prefetch_related('user').all() # 2
#
# project.employees.all() # 3
# ✔️ project.employees.prefetch_related('user').all() # 2
#
# Hopefully optimize successfully
