from django.http import JsonResponse
from rest_framework import generics,permissions,viewsets
from django.shortcuts import render
from . import serilaizers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
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

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category_id')
        if category is not None:
            qs = qs.filter(category = category)
        return qs
    
class TaggedProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serilaizers.ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs.get('tag')  # Use .get() to avoid KeyError
        # If a tag is provided, filter products based on the tag in the tags field
        if tag:
            qs = qs.filter(tags__icontains=tag)  # Case-insensitive search within the tags field
        
        return qs
    
class RelatedProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serilaizers.ProductListSerializer
    pagination_class = None
    
    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs.get('pk')  # Use .get() to avoid KeyError
        actualProduct = models.Product.objects.get(id=product_id)
        # If a tag is provided, filter products based on the tag in the tags field
        if actualProduct:
            qs = qs.filter(category=actualProduct.category).exclude(id=product_id)  # Case-insensitive search within the tags field
        
        return qs

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


@csrf_exempt
def customerLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = models.User.objects.filter(email=email.lower()).first()
        
        if user_obj:
            username = user_obj.username
            user = authenticate(username=username, password=password)
            
            if user is not None:
                return JsonResponse(
                    {
                        'bool': True,
                        'user': user.username
                    },
                    status=200  # HTTP status code 200 for successful authentication
                )
            else:
                return JsonResponse(
                    {
                        'error': 'Invalid credentials'
                    },
                    status=401  # HTTP status code 401 for unauthorized access
                )
        else:
            return JsonResponse(
                {
                    'error': 'User not found'
                },
                status=404  # HTTP status code 404 for user not found
            )


@csrf_exempt
def customerRegister(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('phoneNumber')
        
        user_email = models.User.objects.filter(email=email.lower()).first()
        user_name = models.User.objects.filter(username=userName.lower()).first()
        phoneNumberCheck = models.Customer.objects.filter(phone=phoneNumber).first()
        
        if user_email :
            return JsonResponse(
                {
                    'error': 'Email already exists'
                },
                status=400  # HTTP status code 400 for bad request
            )
        if user_name :
            return JsonResponse(
                {
                    'error': 'Username already exists'
                },
                status=400  # HTTP status code 400 for bad request
            )
        if phoneNumberCheck :
            return JsonResponse(
                {
                    'error': 'Phone number already exists'
                },
                status=400  # HTTP status code 400 for bad request
            )
        
        user = models.User.objects.create_user(
            username=userName,
            email=email,
            first_name=firstName,
            last_name=lastName,
            password=password
        )
        user.save()

        customer = models.Customer.objects.create(
            user = user,
            phone = phoneNumber
        )
        customer.save()
        
        return JsonResponse(
            {
                'bool': True,
                'user': user.username,
                'message': 'User registered successfully'
            },
            status=201  # HTTP status code 201 for successful resource creation
        )
                   
                
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

class CategoryList(generics.ListCreateAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serilaizers.CategorySerializer
    # permission_classes = (permissions.IsAuthenticated,)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serilaizers.CategoryDetailSerializer
