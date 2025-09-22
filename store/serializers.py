from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem    
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
        model = Review
        fields = ['id', 'name', 'description', 'date'] # fields to be serialized
        #read_only_fields = ['id', 'date'] # fields that are read-only and cannot be modified    
        
    def create(self, validated_data):
        product_id = self.context['product_id'] # get the product_id from the context 
        return Review.objects.create(product_id=product_id, **validated_data) # create a new review with the product_id and validated data



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']



class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value):
            raise serializers.ValidationError(
                'No product with the given ID is found')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']




class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

