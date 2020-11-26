from django.urls import path

from .views import index_view
from .views import detail_view


app_name = 'users'

urlpatterns = [
    path('index/', index_view, name='index_url'),
    path('<str:slug>/', detail_view, name='detail_url'),
]
