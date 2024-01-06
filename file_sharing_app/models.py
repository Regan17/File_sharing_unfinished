# file_sharing_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    is_ops_user = models.BooleanField(default=False)

class File(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
    file_url = models.FileField(upload_to='uploads/')
