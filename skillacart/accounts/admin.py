from django.contrib import admin
from .models import Users

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created_at']
    search_fields = ['username', 'email']
    list_filter = ['username', 'email'] 

admin.site.register(Users, UserAdmin)
