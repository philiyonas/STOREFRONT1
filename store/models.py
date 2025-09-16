from django.core.validators import MinValueValidator    
from django.db import models

# Create your models here.

class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')# if a product is deleted the featured product is set to null and the related name is set to + to avoid reverse relation
  
   # def__str_self(self):-
   #
    def __str__(self):
        return self.title
        

                                        #a many-to-one relation; each Collection points to a single Product instance. The related_name='+' tells Django not to create a reverse relation from Product to Collection, which is useful if you don't need to access collections from a product.    
    class Meta:
        ordering=['title'] # default ordering by title
        

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()# percentage discount
    def __str__(self):
        return self.description
    class Meta:
        ordering=['description'] # default ordering by description

    
        

                                        #a many-to-one relation; each Collection points to a single Product instance. The related_name='+' tells Django not to create a reverse relation from Product to Collection, which is useful if you don't need to access collections from a product.    
   


class Product(models.Model):
    title=models.CharField(max_length=255)
    slug = models.SlugField() 
    description=models.TextField(blank=True, null=True) # description can be blank or null
    unit_price=models.DecimalField(
        max_digits=6, decimal_places=2, 
        validators=[MinValueValidator(0.01)]) # price cannot be negative
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')# if a collection is deleted its products are not deleted and an error is raised
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
    membership=models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
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
    product=models.ForeignKey(Product, on_delete=models.PROTECT)# if a product is deleted its order items are not deleted and an error is raised 
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'OrderItem {self.id} - Order {self.order.id} - Product {self.product.title}'
    class Meta:
        db_table ='store_orderitem' # custom table name
        indexes=[
            models.Index(fields=['order']) # index on order for faster search
        ]

class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    #cart_shared=models.BooleanField(default=False)# if true the cart can be shared with other users via a link


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)# if a cart is deleted all its items are deleted as well
    product=models.ForeignKey(Product, on_delete=models.CASCADE)# if a product is deleted all its cart items are deleted as well                
    quantity=models.PositiveSmallIntegerField()

