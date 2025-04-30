from django.contrib.auth.models import AbstractUser
from django.db import models

from core.base_models import BaseModel


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
