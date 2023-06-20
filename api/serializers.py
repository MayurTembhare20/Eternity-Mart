from rest_framework import serializers
from django.contrib.auth.models import User
from cart.models import Cart
from product.models import Product_Category,Products,Product_Image


class UserSerializer(serializers.ModelSerializer):
    """ Serializer For User """
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {
            'password' : {
                'write_only' : True
            }
        }

    def create(self, validated_data):
        """ Override model's serializers - create(POST) method """
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """ Override model's serializers - update(PUT, PATCH) method """
        if validated_data.get('username'):
            instance.username = validated_data['username']
        if validated_data.get('first_name'):
            instance.first_name = validated_data['first_name']
        if validated_data.get('last_name'):
            instance.last_name = validated_data['last_name']
        if validated_data.get('email'):
            instance.email = validated_data['email']
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    """ Serializer for product category """
    class Meta:
        model = Product_Category
        fields = [
            'name',
            'slug',
            'image'
        ]


class ProductImageSerializers(serializers.ModelSerializer):
    """ Serializer For multiple images of Products """
    class Meta:
        model = Product_Image
        fields = ['image']


class ProductSerializers(serializers.ModelSerializer):
    """ Serializer for Products model  """
    """ Connecting to Product_Image """
    Product_Image = ProductImageSerializers(many=True)

    class Meta:
        model = Products
        fields = ['id',
            'product_category',
            'brand',
            'name',
            'slug', 
            'cover_image',
            'price',
            'description',
            'variation',
            'tags',
            'Product_Image'
            ]
        depth=1 


class CartSerializers(serializers.ModelSerializer):
    """ Serializer for Cart model """
    sub_total = serializers.FloatField(read_only = True)
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'product',
            'variation',
            'quantity',
            'sub_total'
        ]
        depth=2