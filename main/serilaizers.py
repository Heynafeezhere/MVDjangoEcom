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
    class Meta:
        model = models.Product
        fields = ['category','vendor','name','description','price','stock_quantity']
        depth = 1

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['category','vendor','name','description','price','stock_quantity']
        depth = 1

#Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id','user','phone','address_line1','address_line2','city','state','zip_code','country']
        depth = 1


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['id','user','phone','address_line1','address_line2','city','state','zip_code','country']
        depth = 1

#Order  
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['id','customer','order_date','status','total_amount','created_at','updated_at']
        depth = 1

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id','order','product','quantity','unit_price','created_at','updated_at']
        depth = 1


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAddress
        fields = ['id','customer','primaryAddress','address_line1','address_line2','city','state','zip_code','country','created_at','updated_at']
        depth = 1
        

