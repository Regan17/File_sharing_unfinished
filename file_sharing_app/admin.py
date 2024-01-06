# file_sharing_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, File

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_ops_user')  # Add other fields you want to display
    search_fields = ('username', 'email')
    ordering = ('username',)
admin.site.register(File)
# Register the custom admin for your CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
