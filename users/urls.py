from django.urls import path

from .views import (
    IndexView, BossDetailView, ProjectDetailView
)


app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index-url'),
    path('boss/<str:slug>/', BossDetailView.as_view(), name='boss-detail'),
    path('project/<str:slug>/', ProjectDetailView.as_view(), name='project-detail'),
]
