"""
URL configuration for storefront1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 
import debug_toolbar 
#urlpatterns is 
admin.site.site_header = "Ethioleap_Storefront Admin"
admin.site.index_title = "Ethioleap_Storefront Admin Portal"
admin.site.site_title = "Ethioleap_Storefront Admin"
admin.site.site_brand = "Ethioleap_Storefront" # type: ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('store.urls')),
    path('store/', include('store.urls', namespace='store')),  # include the store app urls
    #path('collections/<int:pk>/', include('store.urls')),
    path('playground/', include('playground.urls')),# any route that starts with palyground should be routed to playground app and to urls.py module
    path('__debug__/', include('debug_toolbar.urls')), # debug toolbar
]
