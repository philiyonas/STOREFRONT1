from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline    
from tags.models import TaggedItem
from store.admin import ProductAdmin
from store.models import Product
# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 10
    min_num = 1
    max_num = 5

class CustomProductAdmin(ProductAdmin): # Inherit from the existing ProductAdmin by extending it from store.admin
    inlines = [TagInline]  # Inline for tagging products by referencing the TagInline class from tags.admin


# If Product was already registered by the `store` app, unregister it first. Doing this inside a
# try/except prevents import-time AlreadyRegistered errors when both apps import admin modules.
try:
    admin.site.unregister(Product)
    #admin.site.unregister(ProductAdmin)

except admin.sites.NotRegistered:
    pass

# Register the new Product admin with tagging functionality
admin.site.register(Product, CustomProductAdmin)
