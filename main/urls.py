from django.urls import path

from . import views

from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('addresses', views.CustomerAddressViewSet)
routers.register('productratings', views.ProductRatingViewSet)

urlpatterns = [
    path('vendors/', views.VendorList.as_view(), name='VendorList'),
    path('vendor/<int:pk>/', views.VendorDetail.as_view(), name='VendorDetail'),
    path('products/', views.ProductList.as_view(), name='ProductList'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='ProductDetail'),
    path('customers/', views.CustomerList.as_view(), name='customerList'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customerDetail'),
    path('orders/', views.orderList.as_view(), name='orderList'),
    path('order/<int:pk>/', views.orderDetail.as_view(), name='orderDetail'),
    ]

urlpatterns += routers.urls