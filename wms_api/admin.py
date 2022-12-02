from django.contrib import admin

from wms_api.models import Product, Package, ShipmentDetails

# Register your models here.
admin.site.register(Product)
admin.site.register(Package)
admin.site.register(ShipmentDetails)
