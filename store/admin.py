from django.contrib import admin, messages
from django.http import HttpRequest

from tags.models import TaggedItem  
from .models import Collection, Customer, Order, OrderItem, Product, Promotion

#create my own filter for inventory status using To implement a SimpleListFilter

class InventoryFilter(admin.SimpleListFilter):
       # Human-readable title for the filter
        title = 'inventory'
        # Parameter name for the filter in the URL query string
        parameter_name = 'inventory'

        def lookups(self, request, model_admin):
            """
            Returns a list of tuples. Each tuple is (value eg <10 , verbose_name eg low).
            These tuples represent the options displayed in the filter sidebar.
            """
            return [
                
                ('< 10', 'Low'),
                ('> 10', 'Ok'),
            ]
        def queryset(self, request, queryset):
            """
            Returns the filtered queryset based on the selected value.
            """
            if self.value() == '< 10':
                return queryset.filter(inventory__lt=10)
            if self.value() == '> 10':
                return queryset.filter(inventory__gt=10)
            #return queryset # Return unfiltered queryset if no option selected
            


# Register admin classes and models for the store app
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #fields = ['title', 'slug']
    prepopulated_fields = {'slug':['title']}
    exclude = ['promotions']
    list_display=['title', 'unit_price', 'last_update', 'inventory', 'inventory_status','collection_title'] # columns to display in the admin site
    list_editable=['unit_price', 'inventory'] # columns that can be edited in the admin site
    list_per_page=20 # number of items to display per page
    
    search_fields=['title'] # fields to search in the admin site
    list_filter=['last_update', 'collection', InventoryFilter] # fields to filter in the admin site
    autocomplete_fields=['collection'] # fields to autocomplete in the admin site
    
    prepopulated_fields={'slug':('title',)} # automatically populate the slug field based on the title field
    actions=['clear_inventory'] # custom actions to perform on selected items
    list_select_related=['collection'] # optimize query to fetch related collection data

    @admin.display(ordering='collection__title', description='Collection')
    def collection_title(self, product):
        return product.collection.title
    collection_title.admin_order_field='collection' # allow sorting by collection title 
   

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('collection') # optimize query to fetch related collection data
   
    #filter and return by executed methods in my admin product regestration pages
    @admin.display(ordering='inventory', description='Inventory Status')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear Inventories')
    def clear_inventory(self, request, queryset):
        updated_count=queryset.update(inventory=0) # set inventory to 0 for selected items
        self.message_user(request, 
                          f'{updated_count} products were successfully cleared.',
                          messages.ERROR
                          ) # display a message to the user
    #clear_inventory.short_description='Clear inventory' # description of the custom action

   
# Inline model to display order items in the order admin page
# it inherites from admin.TabularInline
#it also allows editing of related models directly within the parent model's admin page
#it has relationship with Order model through ForeignKey
# it is used in OrderAdmin class to display order items in the order admin page
# it is defined outside the OrderAdmin class to keep the code organized and modular
# it implements the display of order items in a tabular format within the order admin interface
class OrderItemInline(admin.TabularInline):
    model = OrderItem                                 # Inline edits OrderItem rows related to an Order
    fk_name = 'order'                                 # FK on OrderItem that links to Order (default name)
    autocomplete_fields = ['product']                 # autocomplete for large product tables
    min_num = 1                                       # require at least one item (optional)
    max_num = 10                                      # limit maximum number of inline forms to 10
    readonly_fields = ['total_price']                 # computed field shown but not editable
    show_change_link = True                           # show link to edit the inline object directly
    extra = 3                                         # don't show extra empty forms

    def total_price(self, obj):                       # computed read-only column for each inline row
        return obj.quantity * obj.unit_price
    total_price.short_description = 'Total'           # column header for total_price
                                         
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer_name']  # columns shown in order list
    list_editable=['payment_status'] # columns that can be edited in the admin site
    list_per_page=10 # number of items to display per page
    list_select_related = ['customer']             # optimize by joining customer
    search_fields=['customer__first_name__istartswith', 'customer__last_name__istartswith'] # fields to search in the admin site
    autocomplete_fields = ['customer']             # use autocomplete widget for customer FK
    list_filter = ['payment_status', 'placed_at']  # filters on the right sidebar
    inlines = [OrderItemInline]                    # show OrderItemInline on the Order edit page
    
    def get_queryset(self, request):
        # select customer and prefetch order items to avoid N+1 queries in the change list / detail
        return super().get_queryset(request).select_related('customer').prefetch_related('orderitem_set')
    
    def customer_name(self, order):                 # display helper column combining first + last name
        return f'{order.customer.first_name} {order.customer.last_name}'
    customer_name.short_description = 'Customer'    # column label



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Display basic customer info plus their most recent order fields
    list_display = ['first_name', 'last_name', 'membership', 'email', 'last_order_placed_at', 'last_order_payment_status']
    list_editable = ['membership']
    list_per_page = 10
    # Only filter by membership here; other order-related filters can be added with custom filters
    list_filter = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    def get_queryset(self, request):
        # Prefetch reverse relation 'order_set' so accessing last order doesn't cause N+1 queries
        return super().get_queryset(request).prefetch_related('order_set')

    def last_order_placed_at(self, customer):
        last = customer.order_set.order_by('-placed_at').first()
        return last.placed_at if last else None
    last_order_placed_at.short_description = 'Last order'
    last_order_placed_at.admin_order_field = 'order__placed_at'

    def last_order_payment_status(self, customer):
        last = customer.order_set.order_by('-placed_at').first()
        return last.payment_status if last else None
    last_order_payment_status.short_description = 'Last payment status'
    last_order_payment_status.admin_order_field = 'order__payment_status'




@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    list_editable = ['quantity', 'unit_price']
    list_select_related = ['order', 'product']
    autocomplete_fields = ['product']

    @admin.display(description='Total')
    def total_price(self, obj):
        return obj.quantity * obj.unit_price

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = []
 
class CollectionAdmin(admin.ModelAdmin):
    # required when another ModelAdmin uses autocomplete_fields to reference Collection
    list_display = ['title','id']
    search_fields = ['title']

    #list_display = ['title']
    # # re-register Collection with its ModelAdmin
admin.site.register(Collection, CollectionAdmin)





