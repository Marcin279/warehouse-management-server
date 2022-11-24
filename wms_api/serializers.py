# from django.contrib.auth.models import User, Group
from wms_api.models import (Package,
                            Product,
                            Modules,
                            Students)

from rest_framework import serializers

"""
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_type', 'category')


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class PackageProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Package
        fields = ('packageType', 'destination', 'products')
        depth = 1


# class PackageCreateSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(many=True)
#     package = PackageProductSerializer()
#
#     class Meta:
#         model = Package
#         fields = ('product', 'package',)


# class AddressDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AddressDetails
#         fields = '__all__'
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
#
#
# class WarehouseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Warehouse
#         fields = '__all__'
#
#
# class WarehouseSummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WarehouseSummary
#         fields = '__all__'
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'


# class ProductStockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductStock
#         fields = '__all__'


# class ProductOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductOrder
#         fields = '__all__'
#
#
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


class ModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules
        fields = ['id', 'module_name', 'module_duration', 'class_room']


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['id', 'name', 'age', 'grade', 'modules']
        depth = 1
