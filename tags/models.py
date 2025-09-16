from django.core.validators import MinValueValidator    
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model): # a simple tag model
    label = models.CharField(max_length=255)  # the name of the tag
    def __str__(self): # string representation of the tag example: "Summer"
        return self.label 
    class Meta:        # meta options for the Tag model used to set default ordering example: alphabetical by label of tag
        ordering = ['label']  # default ordering by label


class TaggedItem(models.Model):    # a through model to link tags to any model example: Product, Collection
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)# the type of the related object (e.g., Product, Collection)
    object_id = models.PositiveIntegerField()# the ID of the related object example: Product, Collection
    content_object = GenericForeignKey('content_type', 'object_id')# the actual related object example: Product, Collection

    def __str__(self):
        return f'{self.tag} tagged to {self.content_object}' # string representation of the tagged item and its related object e.g Product, Collection
    class Meta:
        ordering = ['tag__label']  # default ordering by tag label


