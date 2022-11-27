from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from wms_api.models import (Product,
                            Package,
                            ProductStore,
                            Students,
                            Modules,
                            AddressDetails)
from wms_api.serializers import (
                                 ProductSerializer,
                                 PackageSerializer,
                                 ModulesSerializer,
                                 StudentsSerializer,
                                 AddressDetailsSerializer
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


class AddressDetailsView(APIView):
    """
    List all address_details, or create a new address_details  .
    """

    def get(self, request, format=None):
        address_details = AddressDetails.objects.all()
        serializer = AddressDetailsSerializer(address_details, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data.update({"qrCodeno": "https://www.valentinog.com/blog/drf-request/"})
        serializer = AddressDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailsViewDetails(APIView):
    def get_object(self, pk):
        try:
            return AddressDetails.objects.get(pk=pk)
        except AddressDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        address_details = self.get_object(pk)
        serializer = AddressDetailsSerializer(address_details)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        address_details = self.get_object(pk=pk)
        serializer = AddressDetailsSerializer(address_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        address_details = self.get_object(pk=pk)
        address_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class PackageView(viewsets.ModelViewSet):
    """
    Create new package and add existing
    product/package
    """

    serializer_class = PackageSerializer

    def get_queryset(self):
        package = Package.objects.all()
        return package

    def create(self, request, *args, **kwargs):
        data = request.data

        new_package = Package.objects.create(package_type=data["package_type"],
                                             destination=data["destination"]
                                             )

        new_package.save()

        for product_store in data["product_store"]:
            product_received = product_store["product"]["product_name"]
            product_obj = Product.objects.get(product_name=product_received)  # Fix: ERROR 500
            new_package.products.add(product_obj, through_defaults={"quantity": 3})

        serializer = PackageSerializer(data=new_package)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# ===========================================================================================
# Examples
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
