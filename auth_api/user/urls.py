from django.urls import path 

from .views import create, login, list

urlpatterns = [
    path('create', create, name="create-user"),
    path('login', login),
    path('list', list)
]