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