from django.urls import path 
from django.urls.conf import include
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views
from .views import (CartItemViewSet, CartViewSet, CollectionViewSet, ProductViewSet, ReviewViewSet)   



router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)





products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('products',ProductViewSet, basename='product-details')
products_router.register('reviews', ProductViewSet, basename='product-reviews')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls
app_name = 'store'