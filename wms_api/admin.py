from django.contrib import admin

from wms_api.models import Product, Package, ShipmentDetails, ProductStore, Worker, Warehouse, WarehouseStock

# Register your models here.
admin.site.register(Product)
admin.site.register(Package)
admin.site.register(ShipmentDetails)
admin.site.register(ProductStore)
admin.site.register(Worker)
admin.site.register(Warehouse)
admin.site.register(WarehouseStock)
