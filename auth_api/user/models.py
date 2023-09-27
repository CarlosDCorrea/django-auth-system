from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth.models import BaseUserManager

from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_staff, is_superuser):
        if not email: raise ValueError('User must have an email')
        
        if not username: username = 'default'

        user = self.model(email=self.normalize_email(email), 
                          username=username,
                          is_staff=is_staff, 
                          is_active=True,
                          is_superuser=is_superuser
                          )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username=None, password=None):
        return self._create_user(email, username, password, False, False)

    def create_superuser(self, email, password, username=None):
        return self._create_user(email, username, password, True, True)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email' 
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True 
    
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)