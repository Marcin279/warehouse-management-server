import datetime
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status, viewsets, generics, serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from wms_api.models import (Product,
                            Package,
                            ProductStore,
                            ShipmentDetails)
from wms_api.serializers import (
    ProductSerializer,
    PackageSerializer,
    ShipmentDetailsSerializer, UserSerializer, AllPackageInOneShipmentSerializer
)


# class PackageView(APIView):
#     """
#     List all address_details, or create a new address_details  .
#     """
#
#     def get(self, format=None):
#         product = Package.objects.all()
#         serializer = PackageSerializer(product, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PackageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['qrCodeno'] = "https://www.valentinog.com/blog/drf-request/"
#             serializer.save()
#             # self.perform_create(serializer) # ViewSet
#             # headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ShipmentDetailsView(APIView):
#     """
#     List all address_details, or create a new address_details  .
#     """
#
#     def get(self, request, format=None):
#         address_details = ShipmentDetails.objects.all()
#         serializer = ShipmentDetailsSerializer(address_details, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = ShipmentDetailsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ShipmentDetailsViewDetails(APIView):
#     def get_object(self, pk):
#         try:
#             return ShipmentDetails.objects.get(pk=pk)
#         except ShipmentDetails.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         address_details = self.get_object(pk)
#         serializer = ShipmentDetailsSerializer(address_details)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         address_details = self.get_object(pk=pk)
#         serializer = ShipmentDetailsSerializer(address_details, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         address_details = self.get_object(pk=pk)
#         address_details.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ShipmentDetailsView(viewsets.ModelViewSet):
    serializer_class = ShipmentDetailsSerializer

    def get_queryset(self):
        shipment_details_obj = ShipmentDetails.objects.all()
        return shipment_details_obj


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        return products

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageView(viewsets.ModelViewSet):
    """
    Create new package and add existing
    product/package
    """

    serializer_class = PackageSerializer

    def get_queryset(self):
        package_object = Package.objects.all()
        return package_object

    def create(self, request, *args, **kwargs):
        data = request.data

        new_package = Package.objects.create(package_name=data["package_name"],
                                             package_type=data["package_type"],
                                             sector=data["sector"],
                                             shipment_details=ShipmentDetails.objects.get(
                                                 shipment_name=data["shipment_name"])
                                             )

        for product_store in data["product_store"]:
            product_received = product_store["product_name"]
            product_obj = Product.objects.get(product_name=product_received)
            new_package.products.add(product_obj, through_defaults={"quantity": product_store["quantity"]})

        new_package.save()
        serializer = PackageSerializer(data=new_package)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        package_obj = self.get_object()
        data = request.data

        try:
            for product_store in data["product_store"]:
                product_received = product_store["product"]["product_name"]
                product_obj = Product.objects.get(product_name=product_received)  # Fix: ERROR 500
                package_obj.products.add(product_obj, through_defaults={"quantity": product_store["quantity"]})
        except KeyError:
            pass

        package_obj.sector = data.get("sector", package_obj.sector)
        package_obj.addition_date = datetime.datetime.now()
        package_obj.status = data.get("status", package_obj.status)

        package_obj.save()
        serializer = PackageSerializer(data=package_obj)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WorkerList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser]


class WorkerDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AllPackageInOneShipmentView(APIView):
    def get_object(self, pk):
        try:
            return ShipmentDetails.objects.get(pk=pk)
        except ShipmentDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        shipment_obj = self.get_object(pk=pk)
        shipment = shipment_obj.package_details.all()
        serializer = AllPackageInOneShipmentSerializer(data=list(shipment), many=True)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
