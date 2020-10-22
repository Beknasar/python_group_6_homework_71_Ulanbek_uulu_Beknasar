from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Product, Order


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api_v1:user-detail')

    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'amount', 'price']
        # read_only_fields = ('author',)
