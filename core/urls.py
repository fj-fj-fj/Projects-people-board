from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import SignUpView
from .views import BossSignUpView
from .views import EmployeeSignUpView


urlpatterns = [

    # auth
    path('', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/teamlead/', BossSignUpView.as_view(), name='teamlead_signup'),
    path('signup/employee', EmployeeSignUpView.as_view(), name='employee_signup'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'login/'}, name='logout'),

    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    # FIXME: навести порядок в путях
    path('boss/', include('users.urls')),
    path('project/', include('users.urls'))

]
