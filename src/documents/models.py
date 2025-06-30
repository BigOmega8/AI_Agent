from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL # -> 'auth.User' or custom user model

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(default = 'Title')
    content = models.TextField(default = 'Content')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)