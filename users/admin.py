from django.contrib import admin
from .models import User, Boss, Employee, Project


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'is_boss', 'is_employee', 'is_staff', 'is_superuser'
    )
    list_filter = ('is_boss', 'is_employee')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'leader', 'project')
    list_filter = ('project', 'leader')


class EmployeeInline(admin.TabularInline):
    """ Edit the intermediate model `Employee` inline """
    model = Employee
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    
    def get_heads(self):
        return ', '.join([h.__str__() for h in self.heads.all()])

    get_heads.short_description = 'Руководители'
    list_display = ('title', 'description', get_heads)
    list_filter = ('heads',)
    inlines = (EmployeeInline,)


@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):

    def get_projects(self):
        return ', '.join([p.__str__() for p in self.projects.all()])
    
    get_projects.short_description = 'Проекты'
    list_display = ('user', 'project_completed', get_projects)
    list_filter = ('projects',)
    inlines = (EmployeeInline,)
