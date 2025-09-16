# views.py - request handlers for the store app it is convention to name it views.py but it can be named anything

from django.shortcuts import render, get_object_or_404 
from .models import Product
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 	
from .models import Product
from .serializers import ProductSerializer


@api_view(['GET', 'POST']) # specify allowed methods using my decorator from rest_framework
def product_list(request):
	if request.method == 'GET':
		queryset = Product.objects.all().select_related('collection') # this querry sets all products and their related collection in one go
		serializer =ProductSerializer(queryset , many=True, # this serializes the querryset to json using the ProductSerializer
							     context={'request': request}) # include request in context for HyperlinkedRelatedField
		
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	elif request.method == 'POST':
		deserializer = ProductSerializer(data=request.data) # this deserializes the json data to a python object
		deserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		print(deserializer.validated_data) # access the validated data
		deserializer.save() # save the new product to the database
		return Response(deserializer.data, status=status.HTTP_201_CREATED) # return the serialized data with a 201 status code


@api_view(['GET', 'PUT', 'PATCH'])# specify allowed methods using my decorator from rest_framework
def product_detail(request,id):
	if request.method == 'GET':
		#USING GET_OBJECT_OR_404
		product = get_object_or_404(Product, pk=id)#retrieve a product by its primary key (id) or return a 404 error if not found
		serializer = ProductSerializer(product)#
		return Response(serializer.data)
	elif request.method == 'PUT':
		product = get_object_or_404(Product, pk=id)
		Putdeserializer = ProductSerializer(product, data=request.data) # this deserializes the json data to a python object
		Putdeserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		Putdeserializer.save() # save the updated product to the database
		return Response(Putdeserializer.data) # return the serialized data with a 200 status code
	elif request.method == 'PATCH':
		product = get_object_or_404(Product, pk=id)
		PATCHdeserializer = ProductSerializer(product, data=request.data, partial=True) # this deserializes the json data to a python object
		PATCHdeserializer.is_valid(raise_exception=True)# check if the deserialized data is valid
		PATCHdeserializer.save() # save the updated product to the database
		return Response(PATCHdeserializer.data) # return the serialized data with a 200 status code


@api_view()
def collection_detail(request, pk): # view(request/response handler)for collection detail

	return Response('ok')
	
