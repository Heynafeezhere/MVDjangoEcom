from django.urls import path

from . import views

urlpatterns = [
    path('vendors/', views.VendorList.as_view(), name='VendorList'),
    path('vendor/<int:pk>/', views.VendorDetail.as_view(), name='VendorDetail'),
    path('products/', views.ProductList.as_view(), name='ProductList'),
    path('product/<int:pk>', views.ProductDetail.as_view(), name='ProductDetail'),
]