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
        # read_only_fields = ('category_display',)


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ('id', 'order', 'product', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    product_order = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('user', 'name', 'phone', 'address', 'date_create', 'product_order')
        # fields = ("__all__")

