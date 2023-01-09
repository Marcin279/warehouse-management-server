import string
from django.contrib.auth.models import User
from django.db import models
import random
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


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
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=45)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE, default=Product1)
    # QR_code = models.URLField(max_length=255, default="https://www.google.pl/")
    category = models.CharField(max_length=30, default='Phones')
    QR_code = models.ImageField(blank=True, upload_to='product_qr_code')
    total_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

    def get_qr_code_data(self):
        qr_data: str = f"Product Name: {self.product_name}\nProduct Type: {self.product_type}\nCategory: {self.category}"
        return str(qr_data)

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.get_qr_code_data())
        qr_offset = Image.new('RGB', (500, 500), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.product_name}-{self.id}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.QR_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)


class Package(models.Model):
    REGISTER = 'R'
    PENDING = 'P'
    DONE = 'D'
    REMOVE = 'RM'

    PACKAGE_STATUS = [
        (REGISTER, 'Register'),
        (PENDING, 'Pending'),
        (DONE, 'DONE'),
        (REMOVE, 'REMOVE')
    ]

    # Lista paczek
    package_name = models.CharField(max_length=100,
                                    default="Smartphones")
    package_type = models.CharField(max_length=30)
    qr_code = models.ImageField(blank=True, upload_to='package_qr_code')

    # genenerator
    addition_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sector = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=PACKAGE_STATUS, default=PENDING)
    products = models.ManyToManyField(Product, through='ProductStore')
    shipment_details = models.ForeignKey(ShipmentDetails, related_name='package_details', on_delete=models.SET_NULL,
                                         null=True)

    def __str__(self):
        return self.package_name

    def get_qr_code_data(self):
        qr_data: str = f"Product Name: {self.package_name}\nProduct Type: {self.package_type}\n" \
                       f"Sector: {self.sector}\nStatus: {self.status}\nShipment Details: {self.shipment_details}"
        return str(qr_data)

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.get_qr_code_data())
        qr_offset = Image.new('RGB', (500, 500), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.package_name}-{self.sector}-{self.shipment_details}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)


class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class Worker(models.Model):
    owner = models.OneToOneField('auth.User', related_name='workers', on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.owner.username}, {self.owner.first_name}, {self.owner.last_name}"


class Warehouse(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    warehouse_name = models.CharField(max_length=15)
    products = models.ManyToManyField(Product, through='WarehouseStock')

    def __str__(self):
        return self.warehouse_name


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
