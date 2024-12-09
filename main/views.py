import json
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics,permissions,viewsets
from django.shortcuts import render
from . import serilaizers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from . import CustomPaginations
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
        if 'fetch_limit' in self.request.query_params:
            qs = qs[:int(self.request.query_params['fetch_limit'])]
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
            qs = qs.order_by('-updated_at')
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
                        'userId': user.id,
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
                'userId': user.id,
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

class customerOrderItemList(generics.ListAPIView):
    queryset = models.OrderItem.objects.all()
    serializer_class = serilaizers.OrderItemSerializer
    pagination_class = CustomPaginations.CustomOrderItemListPagination

    # print(queryset)
    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(order__customer__user__id=customer_id)
        qs = qs.order_by('-updated_at')
        return qs
    
    
@csrf_exempt
def orderRequestHandler(request):
    if request.method == 'POST':
        userId = request.POST.get('customer')
        total_amount = request.POST.get('total_amount')
        print(userId)
        user = models.User.objects.filter(id=userId).first()
        if(user == None): 
            return JsonResponse(
                {
                    'error': 'User not found'
                },
                status=404  # HTTP status code 404 for user not found
            )
        customer = models.Customer.objects.filter(user=user).first()
        if(customer == None):
            return JsonResponse(
                {
                    'error': 'User is not a customer'
                },
                status=404  # HTTP status code 404 for user not found
            )
        order = models.Order.objects.create(customer=customer, status='pending', total_amount=total_amount)
        order.save()

        return JsonResponse(
            {
                'bool': True,
                'orderId': order.id
            },
            status=200  # HTTP status code 200 for successful order
        )

@csrf_exempt
def orderItemRequestHandler(request):
   if request.method == 'POST':
        # Read the JSON body of the request
        data = json.loads(request.body)

        # Get the order item array from the payload
        order_item_array = data.get('order', [])
        if not order_item_array:
            return JsonResponse({'error': 'No order items provided'}, status=400)

        # Extract order ID from the first item (assuming all items belong to the same order)
        orderId = order_item_array[0].get('orderId')

        # Fetch the order from the database in a single query
        order = models.Order.objects.filter(id=orderId).first()
        if order is None:
            return JsonResponse({'error': 'Order not found'}, status=404)

        # Collect all product IDs to fetch them in one query
        product_ids = [item['productId'] for item in order_item_array]
        products = models.Product.objects.filter(id__in=product_ids)

        # Create a dictionary for fast lookup by productId
        product_dict = {product.id: product for product in products}

        # Prepare a list to hold OrderItem instances for bulk creation
        order_items_to_create = []

        for item in order_item_array:
            productId = item.get('productId')
            quantity = item.get('quantity')
            unit_price = item.get('unit_price')

            # Check if product exists
            product = product_dict.get(productId)
            if not product:
                return JsonResponse(
                    {'error': f'Product with ID {productId} not found'},
                    status=404
                )

            # Create the OrderItem instance and append to the list
            order_items_to_create.append(
                models.OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price
                )
            )

        # Use Django's bulk_create to insert all the OrderItems in one go
        with transaction.atomic():  # Ensure atomicity of the operation
            models.OrderItem.objects.bulk_create(order_items_to_create)

        # Return a success response
        return JsonResponse(
            {'bool': True, 'message': 'Order items created successfully'},
            status=200
        )

@csrf_exempt
def updateOrderStatusHandler(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        orderId = data.get('orderId')
        orderStatus = data.get('orderStatus')
        transaction_id = data.get('transactionId')
        payment_method = data.get('paymentMethod')

        order = models.Order.objects.filter(id=orderId).first()
        if order is None:
            return JsonResponse({'error': 'Order not found'}, status=404)

        order.status = orderStatus
        order.transaction_id = transaction_id
        order.save()

        return JsonResponse({'bool': True, 'message': 'Order status updated successfully'}, status=200)

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

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by('-updated_at')
        if 'fetch_limit' in self.request.query_params:
            qs = qs[:int(self.request.query_params['fetch_limit'])]
        return qs
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serilaizers.CategoryDetailSerializer
