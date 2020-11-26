from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import BossSignUpForm, EmployeeSignUpForm
from .models import User, Boss, Employee, Project


# NOTE: разобраться с фильтрами и м2м


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'is_boss', 'is_employee', 'is_staff', 'is_superuser'
    ]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'leader', 'project']


class ProjectAdmin(admin.ModelAdmin):
    model = Project

    def get_heads(self):
        return ", " . join([x.__str__() for x in self.heads.all()])

    list_display = ['title', 'description', get_heads]

    get_heads.short_description = 'Руководители'


class MembershipInline(admin.StackedInline):
    model = Project
    filter_horizontal = ('heads',)

class BossAdmin(admin.ModelAdmin):
    list_display = ['user', 'project_completed']


admin.site.register(User, UserAdmin)
admin.site.register (Boss, BossAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project, ProjectAdmin)
