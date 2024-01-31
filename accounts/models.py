from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
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

    transmission_type=(
    ("Manual","Manual"),
    ("Automatic","Automatic"),
    ("CVT","CVT"),
    )

    fuel_type=(
    ("Petrol","Petrol"),
    ("Diesel","Diesel"),
    ("Electric","Electric"),
    )

    vehicle_feature=(
    ("Sunroof","Sunroof"),
    ("GPS","GPS"),
    ("All Wheel drive","All Wheel drive"),
    ("Heated seats","Heated seats"),
    ("Bluetooth","Bluetooth"),
    ("Apple CarPlay","Apple CarPlay"),
    ("Android Auto","Android Auto"),
    ("Backup camera","Backup camera"),
    ("Cruise Control","Cruise Control"),
    ("Push-Button Start","Push-Button Start")
    )

    # Set default features
    default_features = [
        "Sunroof",
        "GPS",
        "Bluetooth"
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    cc = models.CharField(max_length=150, blank=True, null=True)
    year = models.CharField(max_length=150)
    color = models.CharField(max_length=150, default="Black")
    transmission = models.CharField(max_length=150, choices=transmission_type, default='Manual', blank=True, null=True)
    bootCapacity = models.CharField(max_length=150, blank=True, null=True)
    carFuel = models.CharField(max_length=150, choices=fuel_type, default='Petrol', blank=True, null=True)
    features = MultiSelectField(choices=vehicle_feature, default=default_features, max_choices=10, max_length=150, blank=True, null=True)
    location = models.CharField(max_length=100)
    price = models.IntegerField()
    capacity = models.IntegerField()
    CATEGORY_CHOICES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('cycle', 'Cycle'),
    ]
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image2 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image3 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image4 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    image5 = models.ImageField(default='1', upload_to='accounts/vehicle_images')
    bluebookimg = models.ImageField(default='1', upload_to='accounts/bluebookimg')
    citizenimg = models.ImageField(default='1', upload_to='accounts/citizenimg')
    isVerified = models.BooleanField(default=False)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model}"
    
class UserVerificationStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    user_photo = models.ImageField(upload_to='accounts/user_photos', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    citizen_ship_image = models.ImageField(upload_to='accounts/citizenship_images', null=True, blank=True)
    reverify = models.BooleanField(default=True)


@receiver(post_save, sender=UserVerificationStatus)
def send_verification_email(sender, instance, **kwargs):
    if instance.is_verified and not instance.reverify:
        # Send email for verification success
        subject = 'Verification Success'
        message = f'Congratulations! You have been successfully verified and can now make bookings.'
        send_mail(subject, message, 'eliterental.helpline@gmail.com', [instance.user.email])

    elif not instance.is_verified and instance.reverify and instance.user_photo is None:
        # Send email for re-verification
        subject = 'Verification Required'
        message = f'Unfortunately, your verification status has not been done. Please verify to make bookings.'
        send_mail(subject, message, 'eliterental.helpline@gmail.com', [instance.user.email])
    elif not instance.is_verified and instance.reverify and instance.user_photo is not None:
        # Send email for re-verification
        subject = 'Re-verification Required'
        message = f'Unfortunately, your verification status has been reset. Please re-verify to continue making bookings.'
        send_mail(subject, message, 'eliterental.helpline@gmail.com', [instance.user.email])

    def __str__(self):
        return self.user.username