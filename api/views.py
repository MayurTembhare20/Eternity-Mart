from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets, views, response,filters, status,authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from product.models import (Product_Category,Products)
from django.contrib.auth.models import User
from .serializers import (UserSerializer)
from django.db.models import F,Sum
from cart.models import Cart
from . import serializers


class UserAuthView(ObtainAuthToken):
    """ User Authentication API """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserView(viewsets.ModelViewSet):
    """ User CRUD Operation """
    serializer_class = serializers.UserSerializer
    queryset = User.objects.filter(is_superuser=False, is_staff=False)


class ProductCategoryView(views.APIView):
    """ Product Category VIEW """
    serializer_class = serializers.ProductCategorySerializer

    def get(self, request):
        product_categories = Product_Category.objects.filter(status=True)
        serializer = self.serializer_class(product_categories, many=True)
        return response.Response(serializer.data)


class ProductCategoryViewSets(viewsets.ModelViewSet):
    """ Product Category API """
    serializer_class = serializers.ProductCategorySerializer
    queryset = Product_Category.objects.filter(status=True)
    http_method_names = ['get']


class ProductViewSets(viewsets.ModelViewSet):
    """ Products  API """
    serializer_class = serializers.ProductSerializers
    queryset = Products.objects.filter(status=True)
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['product_category__slug']
    ordering_fields = ['price']


class AdditionalInfoCartView(views.APIView):
    """Additional info about current user cart"""
    authentication_classes =  [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        shipping = 50
        discount = 0
        cart_products = Cart.objects.filter(user=request.user).annotate(sub_total=F('product__price') * F('quantity'))
        sub_total = cart_products.aggregate(total=Sum('sub_total'))['total']
        grand_total = sub_total + shipping
        return response.Response({'shipping': shipping,'discount': discount,'sub_total': sub_total,'grand_total':grand_total})


class CartView(views.APIView):
    """ Cart API view """
    authentication_classes =  [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializers

    def get(self,request):
        # queryset = Cart.objects.filter(user=request.user)
        cart_products = Cart.objects.filter(user=request.user).annotate(sub_total=F('product__price') * F('quantity')) 
        serializer = self.serializer_class(cart_products,many=True)
        return response.Response(serializer.data)
    
    def post(self,request):
        """Add to cart"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data.get('quantity')
            product = serializer.validated_data.get('product')
            variation = serializer.validated_data.get('variation')
            cart, is_created = Cart.objects.get_or_create(user=request.user, product=product, variation=variation)
            """get_or_create() : Either it will create object with kwargs or fetch object with given kwargs """
            cart.quantity = quantity
            cart.save()
            return response.Response({'status' :' Success'},status=status.HTTP_200_OK)
        return response.Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,cartId=None):
        try:
            Cart.objects.get(id=cartId).delete()
            return response.Response({'status':'Success'})
        except Cart.DoesNotExist:
            return response.Response({'details':'Not Found'},status=status.HTTP_404_NOT_FOUND)
