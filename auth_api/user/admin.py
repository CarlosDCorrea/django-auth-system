from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'email', 
                    'username', 
                    'password', 
                    'is_staff', 
                    'is_active', 
                    'is_admin', 
                    'is_superuser')