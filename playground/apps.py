#config 
from django.apps import AppConfig

# playground/apps.py is a new file created to define the app configuration for the 'playground' app. 
# This file is necessary for Django to recognize the app and its settings.
# The code below defines the PlaygroundConfig class, which inherits from AppConfig 
# and sets the default_auto_field and name attributes for the app.
# This file is essential for the proper functioning of the 'playground' app within the Django project.
# It should be created in the 'playground' directory.
# playground/apps.py
class PlaygroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'# specifies the type of primary key to use for models in this app.
    name = 'playground' # specifies the name of the app, which should match the directory name of the app.
