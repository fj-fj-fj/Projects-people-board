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
    list_filter = ('project__title', 'leader__user__username')
    # fk_name = "leader"


class ProjectAdmin(admin.ModelAdmin):
    model = Project

    def get_facking_heads(self):
        # print(self.heads)
        return ", " . join([x.__str__() for x in self.heads.all()])

    list_display = ['title', 'description', get_facking_heads]

    get_facking_heads.short_description = 'Руководители'


class MembershipInline(admin.StackedInline):
    model = Project
    filter_horizontal = ('heads',)

class BossAdmin(admin.ModelAdmin):
    list_display = ['user', 'project_completed']
    # save_on_top = True
    # inlines = [
    #     MembershipInline,
    # ]

# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [
#         MembershipInline,
#     ]
#     exclude = ('heads',)


admin.site.register(User, UserAdmin)
admin.site.register (Boss, BossAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project, ProjectAdmin)





# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'author', 'publish',
#                 'status')
#     list_filter = ('status', 'created', 'publish', 'author')
#     search_fields = ('title', 'body')
#     prepopulated_fields = {"slug": ("title",)}
#     raw_id_fields = ('author',)
#     date_hierarchy = 'publish'
#     ordering = ['-publish', 'status']


# admin.site.register(Post, PostAdmin)