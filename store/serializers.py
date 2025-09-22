"""
Serializers for the store app.

Provides DRF ModelSerializers used by the API:
- CollectionSerializer: collection data and optional annotated products_count.
- ProductSerializer: product data with computed price_with_tax, collection relation,
    and custom validation for unit_price.
- ReviewSerializer: creates reviews tied to a product (expects 'product_id' in serializer context).
- SimpleProductSerializer: compact product representation for nesting in cart items.
- CartItemSerializer & CartSerializer: nested cart representations with computed totals.
- AddCartItemSerializer & UpdateCartItemSerializer: input serializers for adding/updating cart items,
    including validation and custom save logic that requires 'cart_id' in context.

These serializers work with models in store.models and Django REST Framework.
"""
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



class SimpleProductSerializer(serializers.ModelSerializer):# simple serializer for nested representation in cart item
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']



class CartItemSerializer(serializers.ModelSerializer):# serializer for cart items
    product = SimpleProductSerializer()#` nested serializer for product details`
    total_price = serializers.SerializerMethodField()# computed field for total price of the cart item

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']



class CartSerializer(serializers.ModelSerializer):# serializer for cart
    id = serializers.UUIDField(read_only=True)# read-only UUID field for cart ID
    items = CartItemSerializer(many=True, read_only=True)# nested serializer for cart items this are called
    total_price = serializers.SerializerMethodField()# computed field for total price of the cart

    def get_total_price(self, cart): # compute total price of the cart by summing total prices of all cart items
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()]) # sum of total prices of all cart items

    class Meta: # meta class defining model and fields of the serializer
        model = Cart
        fields = ['id', 'items', 'total_price']



class AddCartItemSerializer(serializers.ModelSerializer):# serializer for adding items to cart
    product_id = serializers.IntegerField()# input field for product ID

    def validate_product_id(self, value): # custom validation for product ID to ensure it exists
        if not Product.objects.filter(pk=value):
            raise serializers.ValidationError(
                'No product with the given ID is found')
        return value

    def save(self, **kwargs): # custom save method to handle adding items to cart
        cart_id = self.context.get('cart_id')
        if cart_id is None:
            raise serializers.ValidationError("cart_id is required in serializer context.")

        validated_data = getattr(self, 'validated_data', None)
        if not validated_data:
            raise serializers.ValidationError("No validated data. Call is_valid() before save().")

        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity')

        if product_id is None:
            raise serializers.ValidationError({"product_id": "This field is required."})
        if quantity is None:
            raise serializers.ValidationError({"quantity": "This field is required."})

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity # increase quantity if item already in cart
            cart_item.save()# save the updated cart item on the database
            self.instance = cart_item # set the instance to the updated cart item into the serializer instance
        except CartItem.DoesNotExist:
            # create new cart item using explicit fields instead of passing the whole validated_data
            self.instance = CartItem.objects.create(
                cart_id=cart_id, product_id=product_id, quantity=quantity)

        return self.instance

    class Meta: # meta class defining model and fields of the serializer 
        model = CartItem
        fields = ['id', 'product_id', 'quantity']




class UpdateCartItemSerializer(serializers.ModelSerializer): # serializer for updating cart item quantity
    class Meta:
        model = CartItem
        fields = ['quantity']

#delete cart item by the 

