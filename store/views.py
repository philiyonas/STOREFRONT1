from django.shortcuts import render, get_object_or_404 
from .models import Product
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 	
from .models import Product
from .serializers import ProductSerializer


@api_view()
def product_list(request):
	"""Render a page with a list of products.

	- queries all Product objects (use select_related if you have a FK to speed up DB access)
	- passes them to the template context under the key 'products'
	"""
	#products = Product.objects.all().select_related('collection')
	queryset = Product.objects.all().select_related('collection') # this querry sets all products and their related collection in one go
	serializer =ProductSerializer(queryset , many=True, # this serializes the querryset to json using the ProductSerializer
							     context={'request': request}) # include request in context for HyperlinkedRelatedField
	return Response(serializer.data)

	#return render(request, 'store/product_list.html', {'product': product_list})
@api_view()
def product_detail(request,id):
	"""Simple product detail view used from the list page."""
	""" try: 
  		serializer = ProductSerializer(product)
		return Response(serializer.data)
	except Product.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	 """
	#USING GET_OBJECT_OR_404
	product = get_object_or_404(Product, pk=id)#
	serializer = ProductSerializer(product)#
	
	return Response(serializer.data)



@api_view()
def collection_detail(request, pk):
	return Response('ok')
	
