from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Vendor Model.
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)   
    phone =  PhoneNumberField(null=False, blank=False, unique=True)

    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    # Additional Information
    website = models.URLField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

#Product Category Model
class ProductCategory(models.Model):
     # Basic Information
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

#Product Model
class Product(models.Model):
     # Basic Information
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,null=True,related_name='product_category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
#Customer Model
class Customer(models.Model):
    # Basic customer details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone =  PhoneNumberField(null=False, blank=False, unique=True)

    # Additional fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

#Order Model
class Order(models.Model):
    # Link to Customer
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    
    # Order details
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processed', 'Processed'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled')
        ],
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s' % (self.order_date)

#Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

#Customer Address Model
class CustomerAddress(models.Model):
    # Link to Customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="customer_addresses")

    primaryAddress = models.BooleanField(default=False)

    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address_line1