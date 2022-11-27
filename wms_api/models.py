from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    Product1 = 'P1'
    Product2 = 'P2'
    Product3 = 'P3'
    Product4 = 'P4'
    Product5 = 'P5'
    Product6 = 'P6'

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
        return self.product_type


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
    package_type = models.CharField(max_length=30)
    qr_code = models.URLField(max_length=255, default='https://www.google.pl/')  # TODO: Replace default by QR Code

    # genenerator
    admition_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    destination = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=PACKAGE_STATUS, default=PENDING)
    products = models.ManyToManyField(Product, through='ProductStore')

    def __str__(self):
        return self.package_type


class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class Suppliers(models.Model):
    name = models.CharField(max_length=30)


class AddressDetails(models.Model):
    buildings_number = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    address_details = models.ManyToManyField(AddressDetails)


class Warehouse(models.Model):
    address_details = models.ForeignKey(AddressDetails, on_delete=models.CASCADE)
    id_suppliers = models.ForeignKey(Suppliers, on_delete=models.CASCADE)


class WarehouseSummary(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)


class ProductStock(models.Model):
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductOrder(models.Model):
    quantity = models.IntegerField()
    order = models.IntegerField()
    product = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_address_details = models.ForeignKey(AddressDetails, on_delete=models.CASCADE)
    shipment_type = models.CharField(max_length=30)
    creation_date = models.DateTimeField()
    order_col = models.CharField(max_length=30)


class Modules(models.Model):
    module_name = models.CharField(max_length=50)
    module_duaration = models.IntegerField()
    class_room = models.IntegerField()

    def __str__(self):
        return self.module_name


class Students(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.IntegerField()
    modules = models.ManyToManyField(Modules)

    def __str__(self):
        return self.name
