# views.py - request handlers for the store app it is convention to name it views.py but it can be named anything

from django.shortcuts import render, get_object_or_404 
from .models import Product, OrderItem, Collection
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 	
from .models import Product,OrderItem, Collection
from .serializers import ProductSerializer , CollectionSerializer
from django.db.models import Count

from rest_framework.views import APIView

class ProductList(APIView):
	def get(self, request):
		queryset = Product.objects.all().select_related('collection') # this querry sets all products and their related collection in one go
		serializer =ProductSerializer(queryset , many=True, # this serializes the querryset to json using the ProductSerializer
							     context={'request': request}) # include request in context for HyperlinkedRelatedField
		
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		deserializer = ProductSerializer(data=request.data) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		print(deserializer.validated_data) # access the validated data
		deserializer.save() # save the new product to the database
		return Response(deserializer.data, status=status.HTTP_201_CREATED) # return the serialized data with a 201 status code

class ProductDetail(APIView):
	def get(self, request, id):
		product = get_object_or_404(Product, pk=id)#retrieve a product by its primary key (id) or return a 404 error if not found
		serializer = ProductSerializer(product, context={'request': request})# serialize the product to json using the ProductSerializer
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, id):
		product = get_object_or_404(Product, pk=id)
		deserializer = ProductSerializer(product, data=request.data) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		deserializer.save() # save the updated product to the database
		return Response(deserializer.data, status=status.HTTP_200_OK) # return the serialized data with a 200 status code
	
	def patch(self, request, id):
		product = get_object_or_404(Product, pk=id)
		deserializer = ProductSerializer(product, data=request.data, partial=True) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		deserializer.save() # save the updated product to the database
		return Response(deserializer.data, status=status.HTTP_200_OK) # return the serialized data with a 200 status code
	
	def delete(self, request, id):
		product = get_object_or_404(Product, pk=id)
		# check for related OrderItem rows before deleting
		if product.orderitems.count() > 0:
			return Response({'error':'product cannot be deleted b/c it has an order'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
		product.delete()
		return Response(status=status.HTTP_204_NO_CONTENT) # return a 204 status code indicating
		# that the product was successfully deleted and there is no content to return

class CollectionList(APIView):
	def get(self, request):
		collection = Collection.objects.annotate(products_count=Count('products')) # annotate each collection with the count of related products
		serializer = CollectionSerializer(collection, many=True, context={'request': request}) # serialize the collection to json using the CollectionSerializer
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request):
		deserializer = CollectionSerializer(data=request.data) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		deserializer.save() # save the new collection to the database
		return Response(deserializer.data, status=status.HTTP_201_CREATED) # return the serialized data with a 201 status code

class CollectionDetail(APIView):
	def get(self, request, pk):
		collection = get_object_or_404(Collection, pk=pk)
		serializer = CollectionSerializer(collection, context={'request': request}) # serialize the collection to json using the CollectionSerializer
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def put(self, request, pk):
		collection = get_object_or_404(Collection, pk=pk)
		deserializer = CollectionSerializer(collection, data=request.data) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		deserializer.save() # save the updated collection to the database
		return Response(deserializer.data, status=status.HTTP_200_OK) # return the serialized data with a 200 status code
	
	def patch(self, request, pk):
		collection = get_object_or_404(Collection, pk=pk)
		deserializer = CollectionSerializer(collection, data=request.data, partial=True) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		deserializer.save() # save the updated collection to the database
		return Response(deserializer.data, status=status.HTTP_200_OK) # return the serialized data with a 200 status code
	
	def delete(self, request, pk):
		collection = get_object_or_404(Collection, pk=pk)
		if Product.objects.filter(collection=collection).exists():
			return Response({'error':'collection cannot be deleted b/c it has a product'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
		collection.delete()
		return Response(status=status.HTTP_204_NO_CONTENT) # return a 204 status code indicating
		# that the collection was successfully deleted and there is no content to return