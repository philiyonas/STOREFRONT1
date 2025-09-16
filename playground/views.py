#request handler module it does not have to be named views.py but it is a convention
#  b/c it doesn't consist templates or models
from typing import Collection
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from store import models
from store.models import OrderItem, Product, Collection 

def say_hello(request):
    query_set3 = Product.objects.values('title', 'unit_price')[:] # returns a QuerySet of dictionaries with specified fields only
    query_set = Product.objects.select_related('collection').all()[:] # returns a QuerySet of dictionaries with specified fields only

    query_set2 = OrderItem.objects.values_list('quantity')# returns a QuerySet of dictionaries with specified fields only
    #print(list(query_set2))
    return render(request, 'hello.html', {'name': 'Ethioleap', 'products':list(query_set)})  # renders a template and passes a context dictionary to it
        
        # return HttpResponse('Hello World')

