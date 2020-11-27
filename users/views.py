from django.shortcuts import render, get_object_or_404

from users.models import Boss, Project


def index_view(request):
    """Returns all bosses and projects"""

    bosses = Boss.objects.all()
    projects = Project.objects.all()

    context = {
        'bosses': bosses,
        'projects': projects,
    }
    return render(request, 'users/index.html', context)


def detail_view(request, slug):
    """:return: all bosses and employees if a project is selected
       :return: all projects and employees if a person is selected
    """

    if 'boss' in request.path:
        boss = get_object_or_404(Boss, user__slug__iexact=slug)
        projects = boss.projects.all()
        employees = boss.subordinates.all()
        result = boss, projects, 'Проэкты'


    elif 'project' in request.path:
        project = get_object_or_404(Project, slug__iexact=slug)
        heads = project.heads.all()
        employees = project.employees.all()
        result = project, heads, 'Руководители'

    context = {
        'current_boss_or_project': result[0],
        'bosses_or_projects_list': result[1],
        'title': result[2],
        'employees': employees
    }

    return render(request, 'users/detail.html', context)
