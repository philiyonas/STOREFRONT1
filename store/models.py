from django.core.validators import MinValueValidator    
from django.db import models
from django.apps import apps
from uuid import uuid4  


# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='featured_in')
  
   # def__str_self(self):-
   #
    def __str__(self):
        return self.title
        

                                        #a many-to-one relation; each Collection points to a single Product instance. The related_name='+' tells Django not to create a reverse relation from Product to Collection, which is useful if you don't need to access collections from a product.    
    class Meta:
        ordering=['title'] # default ordering by title
        

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()# discount is a float field representing percentage discount e.g. 10.5 for 10.5% discount and it can be refernced in the Product model. e.g. promotions.discount=10.5return self.description
    def __str__(self):# string representation of the model, used in the admin site and in the shel for easy identification of the model instance
        return self.description
    class Meta:# meta class to define model metadata like ordering and verbose name,metadata is not a field metada means data about data example verbose name is metadata about the model
        ordering=['description'] # default ordering by description

   
""" def get_uncategorized_collection_pk():
    Collection = apps.get_model('store', 'Collection')# get the Collection model from the store app
    obj, _ = Collection.objects.get_or_create(title='Uncategorized')# create the collection if it doesn't exist
    return obj.pk
 """
class Product(models.Model):
    title=models.CharField(max_length=255)
    slug = models.SlugField() 
    description=models.TextField(blank=True, null=True)
    unit_price=models.DecimalField(
        max_digits=6, decimal_places=2, 
        validators=[MinValueValidator(0.01)])
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)#auto_now_add?
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        related_name='products',
        blank=True,
        null=True
    )
    promotions=models.ManyToManyField(Promotion, blank=True)# a product can have multiple promotions and a promotion can be applied to multiple products
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title'] # default ordering by title
 
         


class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)  # changed to max_length=1
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table ='store_customer' # custom table name
        indexes=[
            models.Index(fields=['last_name', 'first_name']) # composite index on last name and first name for faster search
        ]
        ordering = ['first_name','last_name'] # default ordering by first name and last name



class Order(models.Model):
    placed_at=models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETE='C'
    PAYMENT_STATUS_FAILED='F'

    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    payment_status=models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT)# if a customer is deleted all their orders are deleted as well
    def __str__(self):
        return f'Order {self.pk} - {self.customer.first_name} {self.customer.last_name}'

    class Meta:
        ordering=['-placed_at'] # default ordering by placed_at descending

class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)# one to many relationship with customer each customer can have multiple addresses and each address belongs to one customer

    def __str__(self):
        return f'{self.street}, {self.city}'
    
    class Meta:
        db_table ='store_address' # custom table name
        indexes=[
            models.Index(fields=['city']) # index on city for faster search
        ]
    
    



class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.PROTECT)# if an order is deleted all its items are not deleted as well and an error is raised 
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'OrderItem {self.pk} - Order {self.order.pk} - Product {self.product.title}'
    class Meta:
        db_table ='store_orderitem' # custom table name
        indexes=[
            models.Index(fields=['order']) # index on order for faster search
        ]



class Review(models.Model):
    '''if a product is deleted all its reviews are deleted as well and 
    related name setted to reviews so we can access reviews of a product via product.reviews.all()''' 
    name=models.CharField(max_length=255)# name of person setting reviews 
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    description=models.TextField()
    date=models.DateField(auto_now_add=True)
    '''string representation of the model, used in the admin site and in the shell 
    for easy identification of the model instance example Review 1 - Product 1 by John Doe'''
    """ def __str__(self):
        return f'Review {self.pk} - {self.product.title} by {self.name}'
    
    class Meta:
        ordering=['-date'] # default ordering by date descending """


class Cart(models.Model):
    #id = models.UUIDField(primary_key=True, default=models.UUIDField) # use UUID for cart id for security reasons
    id = models.UUIDField(primary_key=True, 
                          default=uuid4, editable=False)  # generate UUID with uuid4
    created_at=models.DateTimeField(auto_now_add=True)
    cart_shared=models.BooleanField(default=True)# if true the cart can be shared with other users via a link


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, 
                           on_delete=models.CASCADE, 
                           related_name='items')# if a cart is deleted all its items are deleted as well
    product=models.ForeignKey(Product, on_delete=models.CASCADE)# if a product is deleted all its cart items are deleted as well                
    quantity=models.PositiveSmallIntegerField(validators=[MinValueValidator(1)]
)
    #if product in cart increase quantity instead of adding a new item 
    class Meta:
        unique_together=[['cart', 'product']] # a product can only appear once in a cart consrianes list of list 
        
