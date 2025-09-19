from django.urls import path
from store import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from pprint import pprint

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

pprint(router.urls)
app_name = 'store'

urlpatterns = [
    ####path('collections/<int:pk>/', views.CollectionDetail.as_view()),

]
