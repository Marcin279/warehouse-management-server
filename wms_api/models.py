from django.db import models


# Create your models here.
class Package(models.Model):
    id = models.IntegerField(primary_key=True)
    packageType = models.CharField(max_length=30)
    qrCodeno = models.URLField(max_length=255)
    admitionDate = models.DateTimeField()
    destination = models.IntegerField()

    def __str__(self):
        return {f"id={self.id}, packegeType={self.packageType}"}


