from django.db import models
from django.conf import settings


class VehicleRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    capacity = models.IntegerField()
    CATEGORY_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('cycle', 'Cycle'),
    ]
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100)
    description = models.TextField()
    image1 = models.ImageField(default='1', upload_to='vehicle_images/')
    image2 = models.ImageField(default='1', upload_to='vehicle_images/')
    image3 = models.ImageField(default='1', upload_to='vehicle_images/')
    image4 = models.ImageField(default='1', upload_to='vehicle_images/')
    image5 = models.ImageField(default='1', upload_to='vehicle_images/')
    bluebookimg = models.ImageField(default='1', upload_to='bluebookimg/')
    citizenimg = models.ImageField(default='1', upload_to='citizenimg/')

    def __str__(self):
        return f"{self.brand} {self.model}"