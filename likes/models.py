from django.db import models                        # Django ORM base module for defining model fields and models
from django.contrib.auth.models import User         # Django's built-in User model for referencing users in relations
from django.contrib.contenttypes.models import ContentType  # Model that stores type info for generic relations
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
"""App likes

   liked Items 
   - which user likes which object
   - user : Foriegnkey to User class in (django.contrib.auth.models)
   """

class LikedItem(models.Model):                           # Define a Like model to record that a user liked a specific object
    user = models.ForeignKey(User, on_delete=models.CASCADE) # ForeignKey to User: the user who liked the object; CASCADE deletes likes when the user is deleted
   
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # ForeignKey to ContentType: identifies the model (type) of the liked object
    object_id = models.PositiveIntegerField()      # Integer field storing the primary key of the liked object instance
    content_object = GenericForeignKey() #the actual Object 

