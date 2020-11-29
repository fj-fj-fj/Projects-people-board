from django.urls import path

from .views import IndexView
from .views import BossDetailView
from .views import ProjectDetailView


app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index_url'),
    path('boss/<str:slug>/', BossDetailView.as_view(), name='boss_detail_url'),
    path('project/<str:slug>/', ProjectDetailView.as_view(), name='project_detail_url'),
]
