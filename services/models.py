from django.db import models
from django.conf import settings
from accounts.models import VehicleRegistration
# Create your models here.

class bookInstantly(models.Model):
    st=(
    ("Processing","Processing"),
    ("Accepted","Accepted"),
    ("Cancelled","Cancelled"),
    ("Decline","Decline"),
    ("Done","Done"),
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    pickDate = models.DateField()
    pickTime = models.TimeField()
    dropDate = models.DateField()
    dropTime = models.TimeField()
    status = models.CharField(max_length=150, choices=st, default='Processing')
    vehicle_id = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    

    def __str__(self):
        return f'{self.id} - {self.status}'