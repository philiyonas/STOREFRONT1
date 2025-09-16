
from .models import Tag, TaggedItem
from django.contrib import admin, messages

# Register admin classes and models for the Tags app
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']  # display the label field in the admin list view
    search_fields = ['label'] # add a search box to search by label


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['tag', 'content_object']  # display the tag and related object in the admin list view
    search_fields = ['tag__label', 'content_object__id'] # add a search box to search by tag label and related object ID


admin.site.unregister(TaggedItem) # Unregister the TaggedItem model to avoid duplicate registration
admin.site.unregister(Tag) # Unregister the Tag model to avoid duplicate registration
admin.site.register(TaggedItem, TaggedItemAdmin) # Re-register the TaggedItem model with the admin site
admin.site.register(Tag, TagAdmin) # Re-register the Tag model with the admin site
  