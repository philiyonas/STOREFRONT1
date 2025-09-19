# views.py - request handlers for the store app it is convention to name it views.py but it can be named anything

from django.shortcuts import render, get_object_or_404 
from django.db.models import Count
from django.http import HttpResponse

from .models import Product, OrderItem, Collection
from .models import Product,OrderItem, Collection
from .serializers import ProductSerializer , CollectionSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 	
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.viewsets import ModelViewSet 
#product and products/1/ and collections and collections/1/ with one api view set for each
class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all() # this querry sets all products and their related collection in one go
	serializer_class = ProductSerializer
	
	def get_serializer_context(self):
		return {'request': self.request} # include request in context for HyperlinkedRelatedField
	
	def destroy(self, request, *args, **kwargs):
		if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0 :
			return Response({'error':'product cannot be deleted b/c it has an order'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
		
		return super().destroy(request, *args, **kwargs)
	
class CollectionViewSet(ModelViewSet):
	queryset = Collection.objects.annotate(
		products_count=Count('products')).all() # annotate each collection with the count of related products
	serializer_class = CollectionSerializer

	def get_serializer_context(self):
		return {'request': self.request} # include request in context for HyperlinkedRelatedField
	
	def destroy(self, request, *args, **kwargs):
		collection = get_object_or_404(Collection, pk=kwargs['pk'])
		if Product.objects.filter(collection=collection).exists():
			return Response({'error':'collection cannot be deleted b/c it has a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
		return super().destroy(request, *args, **kwargs)
