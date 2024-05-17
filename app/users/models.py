from django.db import models
from django.contrib.auth.models import AbstractUser


def user_avatar(instance, filename):
    return f"{instance.email}/avatar/{filename}"

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar, null=True, blank=True)