from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class User(AbstractUser):
    email= models.EmailField(unique=True, null=False, blank=False)
  


