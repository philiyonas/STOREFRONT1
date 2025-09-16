from decimal import Decimal
from store.models import Product, Collection 
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    #serializer for the Product model
    #collection = CollectionSerializer(read_only=True)
    
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='store:collection-detail'
        )  
    

    # meta class that defines the model and fields to be serialized
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
    price_with_tax = serializers.SerializerMethodField()
    
    # custom validation method for the serializer
    def validate(self, data):
        """
        Validate that the product's unit price is a positive number and that the inventory is not negative.
        """
        if data['unit_price'] <= 0:
            raise serializers.ValidationError("The unit price must be a positive number.")
        return data
    
    
    def get_price_with_tax(self, product: Product):
        return product.unit_price * Decimal('1.15')
    

    
   
   

   