from django.db import models


# Create your models here.
class PackageModel(models.Model):
    packageType = models.CharField(max_length=30)
    qrCodeno = models.URLField(max_length=255)
    admitionDate = models.DateTimeField()
    destination = models.IntegerField()

    def __str__(self):
        return {f"id={self.id}, packegeType={self.packageType}"}


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


class Category(models.Model):
    name = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=45)
    QR_code = models.URLField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
