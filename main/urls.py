from django.urls import path

from . import views

from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('addresses', views.CustomerAddressViewSet)
routers.register('productratings', views.ProductRatingViewSet)

urlpatterns = [
    #Vendors
    path('vendors/', views.VendorList.as_view(), name='vendorList'),
    path('vendor/<int:pk>/', views.VendorDetail.as_view(), name='vendorDetail'),
    #Products
    path('products/', views.ProductList.as_view(), name='productList'),
    path('products/<str:tag>/', views.TaggedProductList.as_view(), name='taggedProductList'),
    path('product/related-products/<int:pk>/', views.RelatedProductList.as_view(), name='relatedProductList'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='productDetail'),
    #Product Categories
    path('categories/', views.CategoryList.as_view(), name='categoryList'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='categoryDetail'),
    #Customers
    path('customers/', views.CustomerList.as_view(), name='customerList'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customerDetail'),
    path('customer/register/', views.customerRegister, name='custemerRegister'),
    path('customer/login/', views.customerLogin, name='customerLogin'),
    #Orders
    path('orders/', views.orderList.as_view(), name='orderList'),
    path('order/', views.orderRequestHandler, name='orderRequestHandler'),
    path('order/order-item/', views.orderItemRequestHandler, name='orderItemRequestHandler'),
    path('order/<int:pk>/', views.orderDetail.as_view(), name='orderDetail'),
    ]

urlpatterns += routers.urls