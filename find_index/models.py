from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    phone_no = models.BigIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_no']
    
    def __str__(self):
        return self.email
    
    
class Log(models.Model):
    type = models.CharField(max_length=70)
    sub_type = models.CharField(max_length=70)
    shift_name = models.CharField(max_length=70)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name= 'created_by')
    
    
class FindIndex(models.Model):
    log_data = models.JSONField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')