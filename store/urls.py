from django.urls import path 
from django.urls.conf import include
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views

#parent urls conf
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

# parent-child relationship urls conf
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

collections_router = routers.NestedDefaultRouter(router, 'collections', lookup='collection')
#urlpatterns = router.urls + products_router.urls + collections_router.urls
app_name = 'store'

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes defined in the router   
    path('', include(products_router.urls)),
    ####path('collections/<int:pk>/', views.CollectionDetail.as_view()),

]
