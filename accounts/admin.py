from django.contrib import admin

from accounts.models import UserAddress, UserVerificationStatus, VehicleRegistration

# Register your models here.
admin.site.register(UserAddress)
admin.site.register(VehicleRegistration)
admin.site.register(UserVerificationStatus)