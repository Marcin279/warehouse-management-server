import string
from django.contrib.auth.models import User
from django.db import models
import random


# Create your models here.
def generate_package_name():
    letters = string.ascii_lowercase
    return "Package" + "".join(random.choice(letters) for _ in range(10))


class ShipmentDetails(models.Model):
    shipment_name = models.CharField(max_length=50)
    buildings_number = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    total_weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.shipment_name


class Product(models.Model):
    Product1 = 'Product1'
    Product2 = 'Product2'
    Product3 = 'Product3'
    Product4 = 'Product4'
    Product5 = 'Product5'
    Product6 = 'Product6'

    PRODUCT_TYPE = [
        (Product1, 'Product1'),
        (Product2, 'Product2'),
        (Product3, 'Product3'),
        (Product4, 'Product4'),
        (Product5, 'Product5'),
        (Product6, 'Product6')
    ]

    product_name = models.CharField(max_length=45)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE, default=Product1)
    QR_code = models.URLField(max_length=255, default="https://www.google.pl/")
    category = models.CharField(max_length=30, default='Phones')

    def __str__(self):
        return self.product_name


class Package(models.Model):
    REGISTER = 'R'
    PENDING = 'P'
    DONE = 'D'
    SEND = 'S'

    PACKAGE_STATUS = [
        (REGISTER, 'Register'),
        (PENDING, 'Pending'),
        (DONE, 'DONE'),
        (SEND, 'SEND')
    ]

    # Lista paczek
    package_name = models.CharField(max_length=100,
                                    default="Smartphones")
    package_type = models.CharField(max_length=30)
    qr_code = models.URLField(max_length=255, default='https://www.google.pl/')  # TODO: Replace default by QR Code

    # genenerator
    addition_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sector = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=PACKAGE_STATUS, default=PENDING)
    products = models.ManyToManyField(Product, through='ProductStore')
    shipment_details = models.ForeignKey(ShipmentDetails, related_name='package_details', on_delete=models.SET_NULL,
                                         null=True)

    def __str__(self):
        return self.package_name


class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class Worker(models.Model):
    owner = models.ForeignKey('auth.User', related_name='workers', on_delete=models.CASCADE)
    role = models.CharField(max_length=30, null=True, blank=True)


class Warehouse(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    warehouse_name = models.CharField(max_length=15)
    products = models.ManyToManyField(Product, through='WarehouseStock')


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()