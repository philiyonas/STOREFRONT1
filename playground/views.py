#request handler module it does not have to be named views.py but it is a convention
#  b/c it doesn't consist templates or models
from typing import Collection
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from store import models
from store.models import OrderItem, Product, Collection

def say_hello(request):
    query_set3 = Product.objects.values('title', 'unit_price')[1:10] # returns a QuerySet of dictionaries with specified fields only
    query_set = Product.objects.select_related('Collection').all()[:10] # returns a QuerySet of dictionaries with specified fields only

    query_set2 = OrderItem.objects.values_list('quintity')# returns a QuerySet of dictionaries with specified fields only
    #print(list(query_set2))
    return render(request, 'hello.html', {'name': 'Ethioleap', 'products':list(query_set3)})  # renders a template and passes a context dictionary to it
        
        # return HttpResponse('Hello World')


#def say_hello2(request):
    """View function that returns a simple "Hello, World!" response.
    Using the ORM to query the database for products and handle the exception if the product does not exist."""
    # method one: using try/except
    '''try:
        product_query = Product.objects.get(pk=0)  # get the product with primary key 0
        print(product_query)
    except Product.DoesNotExist:
        print('product does not exist')'''

    # method two: using filter to avoid exception handling
    #query_set = Product.objects.values_list('id', 'title','Collection__title') # returns a QuerySet of dictionaries with specified fields only
     #.values() method returns a QuerySet of dictionaries instead of model instances, which can be more efficient if you only need specific fields.
     #.select_related('Collection')  # performs a SQL join and includes the related Collection data in the same query to avoid additional database hits
     #.only('id', 'title', 'Collection__title')  # fetches only the specified fields from the database for efficiency
     #.defer('description', 'last_update', 'inventory', 'unit_price')  # excludes the specified fields from the query to reduce data load
     #.all()  # retrieves all Product records from the database
     #.count()  # returns the total number of Product records in the database
     #.exists()  # returns True if there are any Product records in the database, False otherwise
     #.first()  # returns the first Product record or None if no records exist
     #.last()  # returns the last Product record or None if no records exist
     #.order_by('title')  # orders the products by title in ascending order; use '-title' for descending order
     #.reverse()  # reverses the order of the products in the QuerySet
    #query_set = Product.objects.filter(unit_price__gt=20)  # filters products with a unit price greater than 20
    #query_set = Product.objects.filter(title__icontains='coffee')  # filters products with 'coffee' in the title, case-insensitive lockups
     #.filter(inventory__lt=10)  # filters products with inventory less than 10
     #.filter(Collection__title__icontains='outdoor')  # filters products whose collection title contains 'outdoor', case-insensitive
     #.filter(promotions__description__icontains='15%')  # filters products with promotions that have '15%' in the description, case-insensitive
     #.distinct()  # ensures the QuerySet contains unique products, useful when filtering on many-to-many relationships
     #.select_related('Collection')  # performs a SQL join and includes the related Collection data in the same query to avoid additional database hits
     #.prefetch_related('promotions')  # fetches related promotions in a separate query and joins them in Python to optimize many-to-many relationships
    #query_set = Product.objects.aggregate(models.Avg('unit_price'))  # calculates the average unit price of all products
     #.aggregate(models.Max('unit_price'))  # calculates the maximum unit price among all products
     #.aggregate(models.Min('unit_price'))  # calculates the minimum unit price among all products
     #.aggregate(models.Sum('unit_price'))  # calculates the total sum of unit prices of all products
    #query_set = Product.objects.values('Collection__title').annotate(count=models.Count('id'))  # groups products by collection title and counts the number of products in each collection
     #.values('Collection__title').annotate(avg_price=models.Avg('unit_price'))  # groups products by collection title and calculates the average unit price for each collection
     #.values('Collection__title').annotate(max_price=models.Max('unit_price'))  # groups products by collection title and finds the maximum unit price in each collection
     #.values('Collection__title').annotate(min_price=models.Min('unit_price'))  # groups products by collection title and finds the minimum unit price in each collection
     #.values('Collection__title').annotate(total_inventory=models.Sum('inventory'))  # groups products by collection title and sums the inventory for each collection
     #.select_for_update()  # locks the selected rows for update within a transaction to prevent concurrent modifications
     #.raw('SELECT * FROM store_product WHERE unit_price > %s', [20])  # executes a raw SQL query to fetch products with unit price greater than 20
     #.using('replica')  # directs the query to use a specific database connection named 'replica'
     #.defer('description', 'last_update', 'inventory', 'unit_price')  # excludes the specified fields from the query to reduce data load
     #.only('id', 'title', 'Collection__title')  # fetches only the specified fields from the database for efficiency
     #.select_related('Collection')  # performs a SQL join and includes the related Collection data in the same query to avoid additional database hits
     #.filter(unit_price__gt=20)  # filters products with a unit price greater than 20
     #.order_by('title')  # orders the products by title in ascending order; use '-title' for descending order
     #.all()  # retrieves all Product records from the database
     #.values('id', 'title','Collection__title') # returns a QuerySet of dictionaries with specified fields only
    #query_set = OrderItem.objects.values('product_id').distinct() # returns a QuerySet of dictionaries with specified fields only
    #return render(request, 'hello.html', {'name': 'Yoni', 'products':list(query_set)})  # renders a template and passes a context dictionary to it
    # return HttpResponse('Hello World')