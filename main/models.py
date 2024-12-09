from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

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
    slug = models.CharField(max_length=300,unique=True,null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.TextField(null=True,blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    demoLink = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    def product_tags(self):
        tagList = self.tags.split(',')
        return tagList
    
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
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=30, null=True, blank=True)

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
        return f'{self.address_line1}'

#Product Ratings and Reviews
class ProductRating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='rating_customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    
    title = models.CharField(max_length=100)
    
    review = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Customer : {self.customer.user.username} - {self.title} - {self.rating}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alternative text for the image."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url