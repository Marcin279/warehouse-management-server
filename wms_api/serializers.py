from abc import ABC

from django.contrib.auth.models import User, Group
from wms_api.models import (Package,
                            Product,
                            ShipmentDetails,
                            Warehouse,
                            Worker,
                            WarehouseStock,
                            ProductStore)

from rest_framework import serializers

import datetime


class WorkerCustomSerializer(serializers.ModelSerializer):
    # Only workers with role Worker
    owner_id = serializers.CharField(source='owner.id')
    username = serializers.CharField(source='owner.username')
    first_name = serializers.CharField(source='owner.first_name')
    last_name = serializers.CharField(source='owner.last_name')
    email = serializers.CharField(source='owner.email')

    class Meta:
        model = Worker
        fields = ['owner_id', 'username', 'first_name', 'first_name', 'last_name', 'email', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AllWorkerSerializer(serializers.ModelSerializer):
    workers = UserSerializer()

    class Meta:
        model = Worker
        fields = ('workers', 'role')


# class WorkerSerializer(serializers.ModelSerializer):
#     workers = serializers.PrimaryKeyRelatedField(many=True, queryset=Worker.objects.all())
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email', 'workers']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name', 'product_type', 'QR_code', 'category')


class ProductStoreSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)  # TODO: DELETE
    date_creation = serializers.DateTimeField(default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    class Meta:
        model = ProductStore
        fields = ['product', 'date_creation', 'quantity']


class ShipmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = ('id', 'shipment_name', 'buildings_number', 'street', 'postal_code', 'city',
                  'country', 'total_weight')


class PackageSerializer(serializers.ModelSerializer):
    product_store = ProductStoreSerializer(many=True, source='productstore_set')
    addition_date = serializers.DateTimeField(default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    shipment_details = ShipmentDetailsSerializer()  # TODO: New ADD

    class Meta:
        model = Package
        fields = ('id', 'package_name', 'package_type', 'qr_code', 'addition_date', 'sector', 'status',
                  'product_store', 'shipment_details')

    # # TODO Sprawdź czy ta metoda jest potrzeba
    # def create(self, validated_data):
    #     product_data = validated_data.pop('product_store')
    #     shipment_data = validated_data.pop('shipment_details')
    #     package = Package.objects.create(**validated_data)
    #     for product in product_data:
    #         product = Product.objects.get()


class AllPackageInOneShipmentSerializer(serializers.ModelSerializer):
    addition_date = serializers.DateTimeField(default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    class Meta:
        model = Package
        fields = ('id', 'package_name', 'package_type', 'qr_code', 'addition_date', 'sector', 'status')


class WarehouseSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Warehouse
        fields = ('warehouse_name', 'worker.owner.username', 'worker.owner.first_name', 'worker.owner.last_name',
                  'worker.owner.email', 'products')


class WarehouseStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseStock
        fields = ('warehouse', 'product', 'product_quantity')


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStoreSerializer
        fields = '__all__'
