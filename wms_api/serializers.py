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
    role = serializers.CharField(default=Worker.worker)

    class Meta:
        model = Worker
        fields = ['owner_id', 'username', 'first_name', 'first_name', 'last_name', 'email', 'role']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')


class AllWorkerSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Worker
        fields = ('owner', 'role')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name', 'product_type', 'QR_code', 'category')


class ProductStoreSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)  # TODO: DELETE
    date_creation = serializers.SerializerMethodField(method_name='valid_date')

    class Meta:
        model = ProductStore
        fields = ['product', 'date_creation', 'quantity']

    def valid_date(self, obj):
        obj.date_creation = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return obj.date_creation


class ShipmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = ('id', 'shipment_name', 'buildings_number', 'street', 'postal_code', 'city',
                  'country', 'total_weight')


class PackageSerializer(serializers.ModelSerializer):
    product_store = ProductStoreSerializer(many=True, source='productstore_set')
    addition_date = serializers.SerializerMethodField(method_name='valid_date')
    shipment_details = ShipmentDetailsSerializer()

    class Meta:
        model = Package
        fields = ('id', 'package_name', 'package_type', 'qr_code', 'addition_date', 'sector', 'status',
                  'product_store', 'shipment_details')

    def valid_date(self, obj):
        obj.date_creation = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        return obj.date_creation


class AllPackageInOneShipmentSerializer(serializers.ModelSerializer):
    addition_date = serializers.DateTimeField(default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    class Meta:
        model = Package
        fields = ('id', 'package_name', 'package_type', 'qr_code', 'addition_date', 'sector', 'status')


class WarehouseStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = WarehouseStock
        fields = ('warehouse', 'product', 'product_quantity')


class WarehouseSerializer(serializers.ModelSerializer):
    warehouse_stock = WarehouseStockSerializer(many=True, source='warehousestock_set')
    worker = AllWorkerSerializer(many=False)

    class Meta:
        model = Warehouse
        fields = ('warehouse_name', 'warehouse_stock', 'worker')
