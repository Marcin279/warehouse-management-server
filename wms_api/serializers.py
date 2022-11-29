# from django.contrib.auth.models import User, Group
from wms_api.models import (Package,
                            Product,
                            Modules,
                            Students,
                            ShipmentDetails,
                            Warehouse,
                            Worker,
                            WarehouseStock,
                            ProductStore)

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'product_name', 'product_type', 'QR_code', 'category')


class ProductStoreSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductStore
        fields = ['product', 'date_creation', 'quantity']


class PackageSerializer(serializers.ModelSerializer):
    product_store = ProductStoreSerializer(many=True, source='productstore_set')

    class Meta:
        model = Package
        fields = ('id', 'package_type', 'qr_code', 'admition_date', 'destination', 'status', 'product_store')


class AddressDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseStock
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
