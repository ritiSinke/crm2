from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser

from django.urls import reverse
# Create your models here.

class User(AbstractUser):
    email= models.EmailField(unique=True, null=False, blank=False)
  
    def get_absolute_url(self):
        return reverse( 'user_details', kwargs={"pk": self.pk})
  


