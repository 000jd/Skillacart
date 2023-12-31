from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Users(AbstractUser):
    """
    Custom user model.
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,  
    )
    phone_number = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
