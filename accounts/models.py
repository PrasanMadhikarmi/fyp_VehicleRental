from django.db import models
from django.conf import settings

# Create your models here.
class VehicleImage(models.Model):
    vehicle = models.ForeignKey('VehicleRegistration', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/')

class VehicleRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    CATEGORY_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
    ]
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    description = models.TextField()

    def __str__(self):
        return f"{self.brand} {self.model}"