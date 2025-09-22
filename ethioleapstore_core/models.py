from django.db import models
from django.contrib.auth.models import AbstractUser # to extend the default Abstractuser model 

# Create your models here.
class User(AbstractUser): # custom user model extending the default AbstractUser model
    email = models.EmailField(unique=True) # add a unique email field to the user model