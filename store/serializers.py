from decimal import Decimal
from store.models import Product, Collection, Review 
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    # include annotated products_count when present
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    
    # meta class that defines the model and fields to be serialized
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'inventory', 'price_with_tax', 'collection']
    
    price_with_tax = serializers.SerializerMethodField() # computed field for price with tax using SerializerMethodField 
    
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())# foreign key relationship to the Collection model using PrimaryKeyRelatedField

    
    
    #collection  = CollectionSerializer() # nested serializer for the related collection field
        #collection = serializers.HyperlinkedRelatedField(
            #queryset=Collection.objects.all(),
            #view_name='store:collection-detail'
        #)  
    

    # custom validation method for the serializer that overides the serilacer validator
    def validate(self, data):
        """
        Validate that the product's unit price is a positive number and that the inventory is not negative.
        """
        if data['unit_price'] <= 0:
            raise serializers.ValidationError("The unit price must be a positive number.")
        return data
    
    
    def get_price_with_tax(self, product: Product):

        return Decimal(product.unit_price) * Decimal('1.15')



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'date'] # fields to be serialized
        #read_only_fields = ['id', 'date'] # fields that are read-only and cannot be modified    
    def create(self, validated_data):
        product_id = self.context['product_id'] # get the product_id from the context
        return Review.objects.create(product_id=product_id, **validated_data) # create a new review with the product_id and validated data

