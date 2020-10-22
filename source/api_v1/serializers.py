from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Product, Order, OrderProduct, Category


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v1:user-detail')
    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v1:product-detail')
    category_display = CategorySerializer(many=False, read_only=True, source='category')

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'description', 'category', 'category_display', 'amount', 'price']
        # read_only_fields = ('author',)


# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = ('id', 'order', 'product', 'amount')


# class OrderSerializer(serializers.ModelSerializer):
#     order_products = OrderProductSerializer(many=True, read_only=True)
#     class Meta:
#         model = Order
#         fields = ('user', 'first_name', 'last_name', 'email', 'phone', 'status', 'date_create', 'order_products')

