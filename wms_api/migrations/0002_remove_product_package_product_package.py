# Generated by Django 4.1.3 on 2022-11-24 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wms_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='package',
        ),
        migrations.AddField(
            model_name='product',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='wms_api.package'),
        ),
    ]
