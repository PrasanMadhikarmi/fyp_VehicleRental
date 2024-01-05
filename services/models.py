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
    ("Paid","Paid"),
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
    booking_duration = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0) 
    

    def __str__(self):
        return f'{self.id} - {self.status}'
    
class CustomerPayment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    booking_id= models.ForeignKey('bookInstantly', on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    total_paid_amount = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    commission_per = models.IntegerField(default=0)
    vendor_payment = models.IntegerField(default=0)
    vendor_paid_status = models.BooleanField(default=False)
    vendor_payment_ts = models.DateTimeField(null = True, blank = True)

    def __str__(self):
        return f"{self.booking_id} - {self.payment_amount} - {self.payment_date} - {self.vendor_paid_status}"