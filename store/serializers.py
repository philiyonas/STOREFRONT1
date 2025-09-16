from decimal import Decimal
from store.models import Product, Collection 
from rest_framework import serializers

class CollectionSerializer(serializers.Serializer):
    #products_count = serializers.IntegerField()  # Field to hold the annotated product count
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    
"""     class Meta:
        model = Collection
        fields = ['id', 'title']  # Include products_count for annotated field """

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')  # Map unit_price to price in the API
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    #collection =serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all()) # ForeignKey field represented by its primary key
    #collection =serializers.StringRelatedField() # ForeignKey field represented by its string representation 
    # Example of using a nested serializer
    #collection = CollectionSerializer()  # Example of using a nested serializer
    

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='store:collection-detail'  # Ensure this matches the name of your collection detail view
    )
 
    def calculate_tax(self, product: Product): # custom method to calculate tax-included price external to DB response
        return product.unit_price * Decimal('1.15')  # Example: adding 15% tax to unit_price for external API response
