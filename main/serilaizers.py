from rest_framework import serializers 
from dataclasses import fields
from . import models

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
        fields = ['id','user','phone','customer_addresses']
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


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAddress
        fields = ['id','customer','primaryAddress','address_line1','address_line2','city','state','zip_code','country','created_at','updated_at']
        depth = 1
        
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


