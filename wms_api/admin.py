from django.contrib import admin

from wms_api.models import Modules, Students, Product, Package

# Register your models here.
admin.site.register(Modules)
admin.site.register(Students)
admin.site.register(Product)
admin.site.register(Package)
