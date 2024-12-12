from rest_framework import serializers
from . import models
from django.core.exceptions import ValidationError

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['id','user','description','contact_person','phone','address_line1','address_line2','city','state','zip_code','country','website','created_at','updated_at']
        depth = 1


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['id','user','description','contact_person','phone','address_line1','address_line2','city','state','zip_code','country','website','created_at','updated_at']
        depth = 1
        
class ProductListSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = ['id','category','vendor','name','slug','product_tags','description','price','stock_quantity','product_ratings','image']
        depth = 1

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id','product','image','created_at','alt_text']
        depth = 1

class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        many=True
        model = models.Product
        fields = ['id','category','vendor','name','slug','product_tags','description','price','stock_quantity','product_ratings','product_images','demoLink']
        depth = 1

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','first_name','last_name','username','email']
        depth = 1

#Customer
class CustomerSerializer(serializers.ModelSerializer):
    customer_addresses = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Customer
        fields = ['id','user','phone','customer_addresses']
        depth = 1


class CustomerDetailSerializer(serializers.ModelSerializer):
    customer_addresses = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = models.Customer
        fields = ['id','customer_id','user','phone','customer_addresses','date_joined','last_updated','profile_image']
        depth = 1

#Order  
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','customer','order_date','status','total_amount','transaction_id','payment_method','created_at','updated_at']
        depth = 1

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id','order','product','quantity','unit_price','created_at','updated_at']
        depth = 1

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id','order','product','quantity','unit_price','created_at','updated_at']
        depth = 1


from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError

class CustomerAddressSerializer(serializers.ModelSerializer):
    customer_id = serializers.CharField(source='customer.customer_id')

    class Meta:
        model = models.CustomerAddress
        fields = ['id', 'customer_id', 'primaryAddress', 'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country']

    def create(self, validated_data):
        # Extract customer_id from validated data
        customer_id = validated_data.pop('customer', None)
        customer = models.Customer.objects.get(customer_id=customer_id['customer_id'])

        # Check if there are no addresses for the customer
        existing_addresses = models.CustomerAddress.objects.filter(customer=customer)
        
        # If no address exists, create the new one and make it primary
        if not existing_addresses.exists():
            validated_data['primaryAddress'] = True  # Mark the first address as primary

        # Ensure only one primary address exists for the customer
        elif validated_data.get('primaryAddress', False):
            existing_addresses.update(primaryAddress=False)  # Unmark other addresses as primary

        # Check if the address already exists for this customer
        address_exists = existing_addresses.filter(
            address_line1=validated_data.get('address_line1'),
            address_line2=validated_data.get('address_line2', ''),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zip_code=validated_data.get('zip_code'),
            country=validated_data.get('country')
        ).exists()

        if address_exists:
            raise ValidationError("This address already exists for the customer.")
        
        # Create and return the new CustomerAddress
        return models.CustomerAddress.objects.create(customer=customer, **validated_data)

    def update(self, instance, validated_data):
        # Extract customer_id from validated data
        customer_id = validated_data.pop('customer', None)
        if customer_id:
            customer = models.Customer.objects.get(customer_id=customer_id['customer_id'])
            instance.customer = customer

        # Check if primaryAddress is being set
        if validated_data.get('primaryAddress', False):
            # If primaryAddress is set to True, unmark other addresses as primary
            models.CustomerAddress.objects.filter(customer=instance.customer).exclude(id=instance.id).update(primaryAddress=False)

        # Update the instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def delete(self, instance):
        # Get the customer associated with the address
        customer = instance.customer

        # Delete the address
        instance.delete()

        # If the deleted address was the primary address, assign the next address as primary
        remaining_addresses = models.CustomerAddress.objects.filter(customer=customer)

        # If there are remaining addresses, set the first one as primary
        if remaining_addresses.exists():
            next_primary_address = remaining_addresses.first()
            next_primary_address.primaryAddress = True
            next_primary_address.save()
        return None

        
class ProdctRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['id','customer','product','title','review','rating','created_at','updated_at']
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id','title','description','created_at','updated_at']
        depth = 1


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id','title','description','created_at','updated_at']
        depth = 1

#wishList
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wishlist
        fields = ['id','customer','product','created_at','updated_at']
        depth = 1
