"""views,py  is the request handler module for the store app. It is a convention to name it views.py, but it can be named anything.
This module defines various viewsets for handling requests related to products, collections, reviews, carts, and cart items.
its implemetation uses Django REST Framework to create API endpoints for these resources.
and it interacts with models defined in store.models and serializers in store.serializers.
by using viewsets we can define the common behavior for a set of related views in a single class instead of defining each view separately."""


from django.shortcuts import get_object_or_404 
from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend	
from rest_framework.filters import SearchFilter, OrderingFilter # for search and ordering support
from rest_framework.response import Response
from rest_framework import status 	
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import Product, OrderItem, Collection, Review
from .serializers import ProductSerializer , CollectionSerializer, ReviewSerializer
from .filter import ProductFilter # 
from .pagination import DefaultPagination # custom pagination class for paginating large querysets
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer

class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer # specify the serializer to be used for this viewset
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] # add filtering 
	
	filterset_class = ProductFilter # using custom filter class for more complex filtering
	pagination_class = DefaultPagination  # applying custom pagination class for spesfic viewset instead of globally seting it in settings.py
	search_fields = ['title', 'description'] # enables search by title and description using ?search=keyword
	ordering_fields = ['unit_price', 'last_update'] # allows ordering by unit_price and last update
	
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
	
	
class ReviewViewSet(ModelViewSet):
	queryset =Review.objects.all()
	serializer_class = ReviewSerializer
	# since we have access to review class attributes here we can overide it and add extra field
	# and use it to serializer viewset usning context object  
	def get_queryset(self):
		return Review.objects.filter(product_id=self.kwargs['product_pk'])
	def get_serializer_context(self):
		return {'product_id': self.kwargs['product_pk']} # include request in context for HyperlinkedRelatedField
	def destroy(self, request, *args, **kwargs):
		return super().destroy(request, *args, **kwargs) 
	


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()#queryset with prefetch related to optimize queries by reducing number of queries to get cart items and their products
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')


	
