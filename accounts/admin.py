from django.contrib import admin

from accounts.models import UserAddress, UserVerificationStatus, VehicleRegistration

# Register your models here.
admin.site.register(UserAddress)

class VehicleRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'brand', 'model', 'year', 'isVerified', 'available')
    search_fields = ('brand', 'model', 'year', 'user__username')  # Add other fields as needed
    list_filter = ('isVerified', 'available', 'category')  # Add other fields as needed

admin.site.register(VehicleRegistration, VehicleRegistrationAdmin)


class UserVerificationStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'reverify')
    search_fields = ('user__username', 'is_verified')
    list_filter = ('is_verified', 'reverify')

admin.site.register(UserVerificationStatus, UserVerificationStatusAdmin)