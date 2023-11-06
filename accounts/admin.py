from django.contrib import admin

from accounts.models import UserAddress, VehicleRegistration

# Register your models here.
admin.site.register(UserAddress)
admin.site.register(VehicleRegistration)