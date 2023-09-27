from django.urls import path 

from .views import create, login, list, activate, activate_user_success

urlpatterns = [
    path('create', create, name="create-user"),
    path('activate', activate, name="activate-user"),
    path('activate-success', activate_user_success, name="activate-user-success"),
    path('login', login),
    path('list', list),
]