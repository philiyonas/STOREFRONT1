from django_filters.rest_framework import filterset
from store.models import Product

class ProductFilter(filterset.FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],  # less than and greater than filters for unit_price
        }