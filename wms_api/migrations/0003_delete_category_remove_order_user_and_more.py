# Generated by Django 4.1.3 on 2022-11-24 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wms_api', '0002_remove_product_package_product_package'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user_address_details',
        ),
        migrations.DeleteModel(
            name='ProductOrder',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address_details',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='address_details',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='id_suppliers',
        ),
        migrations.RemoveField(
            model_name='warehousesummary',
            name='warehouse',
        ),
        migrations.DeleteModel(
            name='AddressDetails',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Suppliers',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Warehouse',
        ),
        migrations.DeleteModel(
            name='WarehouseSummary',
        ),
    ]