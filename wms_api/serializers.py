# from django.contrib.auth.models import User, Group
from wms_api.models import (Package,
                            Product,
                            Modules,
                            Students,
                            AddressDetails,
                            Warehouse,
                            User,
                            WarehouseSummary,
                            ProductStock,
                            ProductOrder,
                            Order, Category)

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('package_type', 'qr_code', 'admition_date', 'destination', 'status')


class PackageProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, allow_null=True)  # Allow to null value in field

    class Meta:
        model = Package
        fields = ('package_type', 'destination', 'admition_date', 'products')
        depth = 1


class PackageCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    package = PackageProductSerializer()

    class Meta:
        model = Package
        fields = ('product', 'package',)


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


# ======================================================================
# Examples
class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['id', 'module_name', 'module_duration', 'class_room']


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'name', 'age', 'grade', 'modules']
        depth = 1
