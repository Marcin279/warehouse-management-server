from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet

from wms_api.models import (Product,
                            Package, Students, Modules)
from wms_api.serializers import (PackageProductSerializer,
                                 ProductSerializer, ModulesSerializer, StudentsSerializer
                                 )


class ProductView(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PackageView(APIView):
#     """
#     List all address_details, or create a new address_details  .
#     """
#
#     def get(self, request, format=None):
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['qrCodeno'] = "https://www.valentinog.com/blog/drf-request/"
#             serializer.save()
#             # self.perform_create(serializer) # ViewSet
#             # headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddressDetailsView(APIView):
#     """
#     List all address_details, or create a new address_details  .
#     """
#
#     def get(self, request, format=None):
#         address_details = AddressDetails.objects.all()
#         serializer = AddressDetailsSerializer(address_details, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         request.data.update({"qrCodeno": "https://www.valentinog.com/blog/drf-request/"})
#         serializer = AddressDetailsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddressDetailsViewDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return AddressDetails.objects.get(pk=pk)
#         except AddressDetails.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         address_details = self.get_object(pk)
#         serializer = AddressDetailsSerializer(address_details)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         address_details = self.get_object(pk=pk)
#         serializer = AddressDetailsSerializer(address_details, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         address_details = self.get_object(pk=pk)
#         address_details.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class PackageProductView(APIView):
#     def get(self, request, format=None):
#         package = Package.objects.all()
#         serializer = PackageProductSerializer(package, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#
#         new_package = Package.objects.create(packageType=data["packageType"],
#                                              destination=data["destination"],
#                                              status=data["status"])
#
#         new_package.save()
#
#         for product in data["products"]:
#             product_obj = Package.objects.get(product_type=product["product_type"])
#             new_package.products.add(product_obj)
#
#         serializer = PackageProductSerializer(data=new_package)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# =============================================================================================
# class ProductView(viewsets.ModelViewSet):
#     """
#     List all address_details, or create a new address_details  .
#     """
#     serializer_class = ProductSerializer
#
#     def get_queryset(self):
#         product = Product.objects.all()
#         serializer = PackageProductSerializer(product, many=True)
#         return Response(serializer.data)


class PackageProductView(viewsets.ModelViewSet):
    serializer_class = PackageProductSerializer

    def get_queryset(self):
        package = Package.objects.all()
        return package

    def create(self, request, *args, **kwargs):
        data = request.data

        new_package = Package.objects.create(packageType=data["packageType"],
                                             destination=data["destination"]
                                             )

        new_package.save()

        for product in data["products"]:
            product_obj = Product.objects.get(product_type=product["product_type"])  # Fix: ERROR 500
            # product_obj = get_object_or_404(Product,  product_type=product["product_type"])
            new_package.products.add(product_obj)

        serializer = PackageProductSerializer(data=new_package)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StudentsViewSet(viewsets.ModelViewSet):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        student = Students.objects.all()
        return student

    def create(self, request, *args, **kwargs):
        data = request.data

        new_student = Students.objects.create(
            name=data["name"], age=data['age'], grade=data["grade"])

        new_student.save()

        for module in data["modules"]:
            module_obj = Modules.objects.get(module_name=module["module_name"])
            new_student.modules.add(module_obj)

        serializer = StudentsSerializer(new_student)

        return Response(serializer.data)


class ModulesViewSet(viewsets.ModelViewSet):
    serializer_class = ModulesSerializer

    def get_queryset(self):
        module = Modules.objects.all()
        return module
