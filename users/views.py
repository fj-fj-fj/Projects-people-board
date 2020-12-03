from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from users.models import User, Boss, Project


class IndexView(ListView):
    model = Boss
    template_name = 'users/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # XXX: пересмотреть 
        context['boss_list'] = Boss.objects.all()
        context['project_list'] = Project.objects.all()
        return context


class BossDetailView(DetailView):
    model = Boss
    template_name = 'users/boss_detail.html'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        return User.objects.select_related('boss').get(slug__iexact=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'boss': self.object.boss,
            'project_list': self.object.boss.projects.all(),
            'employee_list': self.object.boss.subordinates.all(),
        })
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'users/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # XXX: пересмотреть 
        project = get_object_or_404(Project, slug__iexact=self.kwargs['slug'])
        context.update({
            'project': project,
            'boss_list': project.heads.all(),
            'employee_list': project.employees.all()
        })
        return context




# NOTE  ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# Great night to stop the deluge of database queries

# если у руководителя 1 сотрудник и 1 проект:

# case 1
# user = User.objects.get(slug__iexact=slug) + boss = Boss.objects.get(user=user) --> connection.queries == 3
# + boss.projects.all() + boss.subordinates.all() --> connection.queries == 5

# case 2
# user = User.objects.prefetch_related('boss__subordinates').prefetch_related('boss__projects').get(slug__iexact=slug) --> connection.queries == 4
# + user.boss.subordinates.all() (+1) + user.boss.projects.all() (+0) --> connection.queries == 5

# case 3
# user = User.objects.select_related('boss').get(slug__iexact=slug) --> connection.queries == 1
# + user.boss.projects.all() + user.boss.subordinates.all() --> connection.queries == 4  win