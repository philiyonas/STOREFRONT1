from django.urls import path
from store import views

app_name = 'store'

urlpatterns = [
    path('products/', views.ProductListCreate.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('collections/', views.CollectionListCreate.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view()),
]
