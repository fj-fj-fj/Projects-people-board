from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import (
    SignUpView, BossSignUpView, EmployeeSignUpView
)


urlpatterns = [

    path('', include('users.urls')),
    path('admin/', admin.site.urls),

    # auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/teamlead/', BossSignUpView.as_view(), name='teamlead-signup'),
    path('signup/employee/', EmployeeSignUpView.as_view(), name='employee-signup'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'login/'}, name='logout'),

]
