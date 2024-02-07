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
        return f"{self.booking_id} - {self.total_paid_amount} - {self.payment_date} - {self.vendor_paid_status}"


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

class PaymentRequest(models.Model):
    payst = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Decline", "Decline"),
    )

    customer_payments = models.ManyToManyField(CustomerPayment, related_name='payment_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    requested_amount = models.IntegerField()
    paid_date = models.DateTimeField(null=True, blank=True)
    request_status = models.CharField(max_length=50, choices=payst, default='Pending')

    def save(self, *args, **kwargs):
        if self.request_status == 'Paid' and self.paid_date is None:
            self.paid_date = timezone.now()
            for payment in self.customer_payments.all():
                # Update payment details
                payment.vendor_payment_ts = timezone.now()
                payment.vendor_paid_status = True
                payment.save()

                subject = 'Payment Confirmation'

                send_mail(subject, 'We have released your awaiting payment', 'eliterental.helpline@gmail.com', [payment.booking_id.vehicle_id.user.email])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment Request for {', '.join(str(payment.booking_id) for payment in self.customer_payments.all())} - Amount: {self.requested_amount} - Status: {self.request_status}"



class vehicleReview(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=0)  # New field for the rating
    vehicle_id = models.ForeignKey(VehicleRegistration, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.vehicle_id.brand}'