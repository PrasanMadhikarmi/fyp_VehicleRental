from django.contrib import admin


from services.models import CustomerPayment, bookInstantly

# Register your models here.
admin.site.register(CustomerPayment)
admin.site.register(bookInstantly)
