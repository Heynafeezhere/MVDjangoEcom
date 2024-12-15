import json
from django.forms import ValidationError
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics,permissions,viewsets,status
from django.shortcuts import render
from . import serilaizers
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from . import CustomPaginations
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
# Create your views here.
class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serilaizers.VendorSerializer
    # permission_classes = (permissions.IsAuthenticated,)

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serilaizers.VendorDetailSerializer


@csrf_exempt
def vendorRegister(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        userName = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        description = request.POST.get('description')
        contact_person = request.POST.get('contact_person')
        phoneNumber = request.POST.get('phone')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        country = request.POST.get('country')
        website = request.POST.get('website')

        user_email = models.User.objects.filter(email=email.lower()).first()
        user_name = models.User.objects.filter(username=userName.lower()).first()
        phoneNumberCheck = models.Vendor.objects.filter(phone=phoneNumber).first()

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

        vendor = models.Vendor.objects.create(
            user = user,
            description = description,
            contact_person = contact_person,
            address_line1 = address_line1,
            address_line2 = address_line2,
            city = city,
            state = state,
            zip_code = zip_code,
            country = country,
            website = website,
            phone = phoneNumber
        )
        vendor.save()

        return JsonResponse(
            {
                'bool': True,
                'user': user.username,
                'userId': user.id,
                'message': 'User registered successfully'
            },
            status=201  # HTTP status code 201 for successful resource creation
        )



@csrf_exempt
def vendorLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Fetch the user object based on email
        user_obj = models.User.objects.filter(email=email.lower()).first()

        if user_obj:
            username = user_obj.username
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if the user is a vendor
                vendor_obj = models.Vendor.objects.filter(user=user).first()
                if vendor_obj:
                    return JsonResponse(
                        {
                            'bool': True,
                            'userId': vendor_obj.id,
                            'user': user.username,
                            'userType': 'vendor'  # Indicate that this is a vendor
                        },
                        status=200  # HTTP status code 200 for successful authentication
                    )
                else:
                    return JsonResponse(
                        {
                            'error': 'User is not a vendor'
                        },
                        status=404  # HTTP status code 404 for user not found
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

    def vendor_products(self):
        qs = super().get_queryset()
        vendor_id = self.kwargs['pk']
        qs = qs.filter(vendor__id=vendor_id)
        return qs

class productImages(generics.ListCreateAPIView):
    queryset = models.ProductImage.objects.all()
    serializer_class = serilaizers.ProductImageSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs['product_id']
        vendor_id = self.kwargs['vendor_id']
        qs = qs.filter(product__id=product_id,product__vendor__id=vendor_id)
        return qs



@csrf_exempt
def addProduct(request):
    if request.method == 'POST':        
        # Extract vendor and category information
        vendorId = request.POST.get('vendor')
        vendor = models.Vendor.objects.filter(id=vendorId).first()
        
        categoryId = request.POST.get('category')
        category = models.ProductCategory.objects.filter(id=categoryId).first()

        # Return error if vendor or category is not found
        if vendor is None:
            return JsonResponse({'bool': False, 'message': 'Vendor not found'}, status=404)
        
        if category is None:
            return JsonResponse({'bool': False, 'message': 'Category not found'}, status=404)
        
        # Extract and validate product fields
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        item_id = request.POST.get('item_id')
        slug = request.POST.get('slug')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        tags = request.POST.get('tags', '')
        image = request.FILES.get('image', None)

        # Basic validation of required fields
        if not name or not price or not stock_quantity:
            return JsonResponse({'bool': False, 'message': 'Name, price, and stock quantity are required fields'}, status=400)

        try:
            price = float(price)  # Ensure price is a float
        except ValueError:
            return JsonResponse({'bool': False, 'message': 'Invalid price format'}, status=400)
        
        try:
            stock_quantity = int(stock_quantity)  # Ensure stock_quantity is an integer
        except ValueError:
            return JsonResponse({'bool': False, 'message': 'Invalid stock quantity format'}, status=400)

        # Create the product
        try:
            product = models.Product.objects.create(
                vendor=vendor,
                category=category,
                name=name,
                item_id=item_id,
                slug=slug,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                tags=tags,
                image=image
            )
            
            product.save()  # Save the product to the database

            return JsonResponse({'bool': True, 'product_id': product.id, 'message': 'Product added successfully'}, status=201)
        
        except ValidationError as e:
            return JsonResponse({'bool': False,  'message': f'Error creating product: {str(e)}'}, status=400)

    return JsonResponse({'bool': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def updateProduct(request, pk):
    if request.method == 'PUT':
        # Parse the request body as JSON
        body = request.body.decode('utf-8')
        data = json.loads(body)
        
        vendorId = data.get('vendor')
        vendor = models.Vendor.objects.filter(id=vendorId).first()
        
        categoryId = data.get('category')
        category = models.ProductCategory.objects.filter(id=categoryId).first()

        if vendor is None:
            return JsonResponse({'bool': False, 'message': 'Vendor not found'}, status=404)
        
        if category is None:
            return JsonResponse({'bool': False, 'message': 'Category not found'}, status=404)
        
        # Extract product fields
        name = data.get('name')
        description = data.get('description', '')
        itemId = data.get('item_id')
        slug = data.get('slug')
        price = data.get('price')
        stock_quantity = data.get('stock_quantity')
        tags = data.get('tags', '')
        image = data.get('image', None)

        # Basic validation of required fields
        if not name or not price or not stock_quantity:
            return JsonResponse({'bool': False, 'message': 'Name, price, and stock quantity are required fields'}, status=400)

        try:
            price = float(price)  # Ensure price is a float
        except ValueError:
            return JsonResponse({'bool': False, 'message': 'Invalid price format'}, status=400)
        
        try:
            stock_quantity = int(stock_quantity)  # Ensure stock_quantity is an integer
        except ValueError:
            return JsonResponse({'bool': False, 'message': 'Invalid stock quantity format'}, status=400)

        # Handling image upload via request.FILES
        uploaded_image = request.FILES.get('image')  # This will get the file from the request
        image_url = None
        
        if uploaded_image:
            # Save the image to the media directory
            image_name = default_storage.save(f'product_images/{uploaded_image.name}', uploaded_image)
            image_url = default_storage.url(image_name)  # This will return the URL of the uploaded image

        # Update the product
        try:
            product = models.Product.objects.filter(id=pk, vendor=vendor).first()
            if not product:
                return JsonResponse({'bool': False, 'message': 'Product not found'}, status=404)

            product.name = name
            product.slug = slug
            product.description = description
            product.item_id = itemId
            product.price = price
            product.stock_quantity = stock_quantity
            product.tags = tags
            product.category = category

            # Update the image if a new one is uploaded
            if image_url:
                product.image = image_url  # Save the new image URL
            
            product.save()

            return JsonResponse({'bool': True, 'message': 'Product updated successfully'}, status=200)
        
        except ValidationError as e:
            return JsonResponse({'bool': False, 'message': f'Error updating product: {str(e)}'}, status=400)

    return JsonResponse({'bool': False, 'message': 'Invalid request method'}, status=405)
    
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

    def get_object(self):
        # Override get_object to get by customer_id instead of pk
        product_id = self.kwargs.get('pk')
        print(product_id)
        try:
            return models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            raise NotFound(detail="No Product matches the given query.")

    

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serilaizers.UserDetailSerializer

class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serilaizers.CustomerSerializer
    # permission_classes = (permissions.IsAuthenticated,)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serilaizers.CustomerDetailSerializer
    
    def get_object(self):
        # Override get_object to get by customer_id instead of pk
        customer_id = self.kwargs.get('pk')
        try:
            return models.Customer.objects.get(customer_id=customer_id)
        except models.Customer.DoesNotExist:
            raise NotFound(detail="No Customer matches the given query.")
        

@csrf_exempt
def customerLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Fetch the user object based on email
        user_obj = models.User.objects.filter(email=email.lower()).first()

        if user_obj:
            username = user_obj.username
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if the user is a customer
                customer_obj = models.Customer.objects.filter(user=user).first()
                if customer_obj:
                    return JsonResponse(
                        {
                            'bool': True,
                            'userId': user.id,
                            'user': user.username,
                            'userType': 'customer'  # Indicate that this is a customer
                        },
                        status=200  # HTTP status code 200 for successful authentication
                    )
                else:
                    return JsonResponse(
                        {
                            'error': 'User is not a customer'
                        },
                        status=404  # HTTP status code 404 for user not found
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
        data = json.loads(request.body)

        order_item_array = data.get('order', [])
        if not order_item_array:
            return JsonResponse({'error': 'No order items provided'}, status=400)

        orderId = order_item_array[0].get('orderId')

        order = models.Order.objects.filter(id=orderId).first()
        if order is None:
            return JsonResponse({'error': 'Order not found'}, status=404)

        product_ids = [item['productId'] for item in order_item_array]
        products = models.Product.objects.filter(id__in=product_ids)

        product_dict = {product.id: product for product in products}

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
        order.payment_method = payment_method
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

class CustomerWishlist(generics.ListCreateAPIView):
    queryset = models.Wishlist.objects.all()
    serializer_class = serilaizers.WishlistSerializer
    pagination_class = CustomPaginations.CustomOrderItemListPagination

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(customer__customer_id=customer_id)
        qs = qs.order_by('-updated_at')
        return qs


@csrf_exempt
def addToWishlist(request):
    if request.method == 'POST':
        customerId = request.POST.get('customerId')
        productId = request.POST.get('productId')

        customer = models.Customer.objects.filter(customer_id=customerId).first()
        
        if customer is None :
            return JsonResponse(
                {
                    'error': 'No such customer Found'
                },
                status=404 
            )
        
        product = models.Product.objects.filter(id=productId).first()

        if product is None :
            return JsonResponse(
                {
                    'error': 'No such product found'
                },
                status=404  
            )
        
        wishlist_exists = models.Wishlist.objects.filter(customer = customer, product=product).exists()

        if(wishlist_exists):
            return JsonResponse(
                {
                    'error': 'product already added to wishlist'
                },
                status=400
            )
        
        wishlist = models.Wishlist.objects.create(
            customer=customer,
            product=product,
        )
        wishlist.save()


        return JsonResponse(
            {
                'bool': True,
                'message': 'Wishlist Added successfully'
            },
            status=201  # HTTP status code 201 for successful resource creation
        )

@csrf_exempt
def checkWishlist(request):
    customerId = request.GET.get('customerId')
    productId = request.GET.get('productId')
    
    if customerId is None or productId is None:
        return JsonResponse(
            {
                'error': 'Missing required parameters'
            },
            status=400
        )

    wishlist_exists = models.Wishlist.objects.filter(customer__user__id = customerId, product__id=productId).exists()
    
    return JsonResponse(
        {
            'bool': wishlist_exists
        },
        status=200
        )

@csrf_exempt
def reomveFromWishlist(request,wishlistId):
    if request.method == 'DELETE':
        wishlist_exists = models.Wishlist.objects.filter(id = wishlistId).first()
    
        if(wishlist_exists):
            wishlist_exists.delete()
            return JsonResponse(
                    {'bool': True, 'message': 'Product removed from wishlist successfully'},
                    status=200
                )
        return JsonResponse(
            {
                'error': 'Item not found'
            },
            status=404
            )
        
class CustomerAddressList(generics.ListCreateAPIView):
    queryset = models.CustomerAddress.objects.all()
    serializer_class = serilaizers.CustomerAddressSerializer
    pagination_class = CustomPaginations.CustomAddressListPagination

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(customer__customer_id=customer_id)
        qs = qs.order_by('-updated_at')
        return qs

def customerDashboard(request,customer_id):
    addressCount = models.CustomerAddress.objects.filter(customer__customer_id = customer_id).count()
    wishlistCount = models.Wishlist.objects.filter(customer__customer_id = customer_id).count()
    orderCount = models.OrderItem.objects.filter(order__customer__customer_id = customer_id).count()

    return JsonResponse(
        {
            'addressCount': addressCount,
            'wishlistCount': wishlistCount,
            'ordersCount': orderCount    
    },status=200)
