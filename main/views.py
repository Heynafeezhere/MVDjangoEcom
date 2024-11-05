from rest_framework import generics,permissions,viewsets
from django.shortcuts import render
from . import serilaizers
from . import models

# Create your views here.
class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serilaizers.VendorSerializer
    # permission_classes = (permissions.IsAuthenticated,)

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serilaizers.VendorDetailSerializer
    
class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serilaizers.ProductListSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serilaizers.ProductDetailSerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serilaizers.CustomerSerializer
    # permission_classes = (permissions.IsAuthenticated,)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serilaizers.CustomerDetailSerializer

class orderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serilaizers.OrderSerializer

class orderDetail(generics.ListAPIView):
    # queryset = models.OrderItem.objects.all()
    serializer_class = serilaizers.OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        filtered_order = models.Order.objects.get(id=order_id)
        return models.OrderItem.objects.filter(order=filtered_order)

class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serilaizers.CustomerAddressSerializer

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = models.ProductRating.objects.all()
    serializer_class = serilaizers.ProdctRatingSerializer
