import datetime
import http.client

from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, viewsets, generics, serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from wms_api.models import (Product,
                            Package,
                            ProductStore,
                            ShipmentDetails, Warehouse, Worker, WarehouseStock)
from wms_api.serializers import (
    ProductSerializer,
    PackageSerializer,
    ShipmentDetailsSerializer, AllPackageInOneShipmentSerializer, WarehouseSerializer,
    WorkerCustomSerializer, AllWorkerSerializer, WarehouseStockSerializer
)


class ShipmentDetailsViewDetails(APIView):
    def get_object(self, pk):
        try:
            return ShipmentDetails.objects.get(pk=pk)
        except ShipmentDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        address_details = self.get_object(pk)
        serializer = ShipmentDetailsSerializer(address_details)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        address_details = self.get_object(pk=pk)
        serializer = ShipmentDetailsSerializer(address_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address_details = self.get_object(pk=pk)
        address_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShipmentDetailsView(viewsets.ModelViewSet):
    serializer_class = ShipmentDetailsSerializer

    def get_queryset(self):
        shipment_details_obj = ShipmentDetails.objects.all()
        return shipment_details_obj

    def create(self, request, *args, **kwargs):
        serializer = ShipmentDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    # TODO: Solve serialization error
    def create(self, request, *args, **kwargs):
        data = request.data

        new_package = Package.objects.create(package_name=data["package_name"],
                                             package_type=data["package_type"],
                                             sector=data["sector"],
                                             shipment_details=ShipmentDetails.objects.filter(
                                                 shipment_name=data["shipment_name"]).first()
                                             )

        for product_store in data["product_store"]:
            product_received = product_store["product_name"]
            product_obj = Warehouse.objects.get(product_name=product_received)
            new_package.products.add(product_obj, through_defaults={"quantity": product_store["quantity"]})

        new_package.save()
        serializer = PackageSerializer(data=new_package)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)  # TODO: Remove status

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)  # TODO: Remove status


class WarehouseView(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        warehouse_obj = Warehouse.objects.all()
        return warehouse_obj

    # TODO: Solve serialization error
    def create(self, request, *args, **kwargs):
        data = request.data
        if self.check_if_user_does_not_exist(data["worker_username"]):
            return Response({"Message: User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = User.objects.filter(username=data["worker_username"]).first()

        if self.check_if_warehouse_does_not_exist(data["warehouse_name"]):
            new_warehouse = Warehouse.objects.create(warehouse_name=data["warehouse_name"],
                                                     worker=Worker.objects.get(owner=user))
        else:
            return Response({"Message: Warehouse already exists"}, status=status.HTTP_403_FORBIDDEN)

        for warehouse_stock in data["warehouse_stock"]:
            product_received = warehouse_stock["product_name"]
            product_obj = Product.objects.filter(product_name=product_received).first()
            new_warehouse.products.add(product_obj,
                                       through_defaults={"product_quantity": warehouse_stock["product_quantity"]})

        new_warehouse.save()
        serializer = WarehouseSerializer(data=new_warehouse)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        warehouse = self.get_object()
        data = request.data

        for warehouse_stock in data["warehouse_stock"]:
            product_received = warehouse_stock["product_name"]
            product_object = Product.objects.filter(product_name=product_received).first()
            warehouse.products.add(product_object,
                                   through_defaults={"product_quantity": warehouse_stock["product_quantity"]})

        warehouse.save()

        serializer = WarehouseSerializer(data=warehouse)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def check_if_warehouse_does_not_exist(self, warehouse_name: str) -> bool:
        try:
            warehouse = Warehouse.objects.get(warehouse_name=warehouse_name)
            result = False
        except ObjectDoesNotExist:
            result = True
        return result

    def check_if_user_does_not_exist(self, username: str) -> bool:
        try:
            user = User.objects.get(username=username)
            result = False
        except ObjectDoesNotExist:
            result = True
        return result


class WorkerList(generics.ListAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerCustomSerializer
    # permission_classes = [IsAdminUser]


class AllWorkerView(viewsets.ModelViewSet):
    serializer_class = AllWorkerSerializer

    def get_queryset(self):
        worker_object = Worker.objects.all()
        return worker_object

    def create(self, request, *args, **kwargs):
        data = request.data

        worker = User.objects.filter(username=data["username"])

        if len(worker) == 0:  # If User Does Not Exist
            user = User.objects.create(username=data["username"],
                                       first_name=data["first_name"],
                                       last_name=data['last_name'],
                                       password=data["password"],
                                       email=data['email'],
                                       is_staff=False,
                                       is_active=True,
                                       is_superuser=False)
            Worker.objects.create(owner=user, role=Worker.worker)

            return Response({"Message: Worker account create correctly from user model"})
        else:
            # Worker.objects.create(owner=worker.first(), role=Worker.worker)

            return Response({"Message: User already exist"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


class WarehouseStockView(viewsets.ModelViewSet):
    serializer_class = WarehouseStockSerializer

    def get_queryset(self):
        warehouse_stock = WarehouseStock.objects.all()
        return warehouse_stock


class DashboardView(APIView):
    def get(self, request):
        return Response({"Message": "True"})
