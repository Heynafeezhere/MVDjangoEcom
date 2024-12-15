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
    path('vendor/register/', views.vendorRegister, name='vendorRegister'),
    path('vendor/login/', views.vendorLogin, name='vendorLogin'),
    path('vendor/<int:pk>/products/', views.ProductList.as_view(), name='vendorProductList'),
    path('vendor/<int:vendor_id>/products/<int:product_id>/images/', views.productImages.as_view(), name='productImages'),


    #Products
    path('products/', views.ProductList.as_view(), name='productList'),
    path('products/add-product/', views.addProduct, name='addProduct'),
    path('products/product-images/', views.productImages.as_view(), name='productImages'),
    path('products/update-product/<int:pk>/', views.ProductDetail.as_view(), name='updateProduct'),
    path('products/<str:tag>/', views.TaggedProductList.as_view(), name='taggedProductList'),
    path('product/related-products/<int:pk>/', views.RelatedProductList.as_view(), name='relatedProductList'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='productDetail'),
    #Product Categories
    path('categories/', views.CategoryList.as_view(), name='categoryList'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='categoryDetail'),

    #Users
    path('user/<int:pk>/', views.UserDetail.as_view(), name='userDetail'),


    #Customers
    path('customers/', views.CustomerList.as_view(), name='customerList'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customerDetail'),
    path('customer/register/', views.customerRegister, name='custemerRegister'),
    path('customer/login/', views.customerLogin, name='customerLogin'),
    path('customer/address-list/<int:pk>/', views.CustomerAddressList.as_view(), name='customerAddressList'),
    path('customer/<int:pk>/wishlist/', views.CustomerWishlist.as_view(), name='wishlist'),
    path('customer/check-wishlist/', views.checkWishlist, name='checkwishlist'),
    path('customer/add-wishlist/', views.addToWishlist, name='addTowishlist'),
    path('customer/remove-wishlist/<int:wishlistId>', views.reomveFromWishlist, name='reomveFromWishlist'),
    path('customer/<int:pk>/orders/', views.customerOrderItemList.as_view(), name='customerOrderItemList'),
    path('customer/dashboard/<int:customer_id>/', views.customerDashboard, name='customerDashboard'),


    #Orders
    path('orders/', views.orderList.as_view(), name='orderList'),
    path('order/', views.orderRequestHandler, name='orderRequestHandler'),
    path('order/<int:pk>/', views.orderDetail.as_view(), name='orderDetail'),
    path('order/order-item/', views.orderItemRequestHandler, name='orderItemRequestHandler'),
    path('order/update-order-status/', views.updateOrderStatusHandler, name='updateOrderStatusHandler'),
    ]


urlpatterns += routers.urls