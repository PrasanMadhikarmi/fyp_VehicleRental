from django.db import models
from django.conf import settings

class UserAddress(models.Model):
    country_choices=(
    ("Nepal","Nepal"),
    )

    user_info= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   
    address = models.CharField(max_length=150)
    street = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=150, choices=country_choices, default='Nepal')
    
    def __str__(self):
        return f'{self.user_info.id} -- {self.user_info.first_name} {self.user_info.last_name} -- {self.user_info.email}'
    
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
    image1 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image2 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image3 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image4 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image5 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    bluebookimg = models.ImageField(default='1', upload_to='accounts/bluebookimg')
    citizenimg = models.ImageField(default='1', upload_to='accounts/citizenimg')
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} {self.model}"