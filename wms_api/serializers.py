# from django.contrib.auth.models import User, Group
from wms_api.models import (PackageModel,
                            AddressDetails,
                            User,
                            Warehouse,
                            WarehouseSummary,
                            Product,
                            ProductStock,
                            ProductOrder,
                            Order,
                            Category)
# from wms_api.models import PackageModel
from rest_framework import serializers


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageModel
        fields = '__all__'


class AddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDetails
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class WarehouseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseSummary
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = '__all__'


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
