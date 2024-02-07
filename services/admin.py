from django.contrib import admin


from services.models import CustomerPayment, bookInstantly, PaymentRequest

# Register your models here.
admin.site.register(CustomerPayment)
admin.site.register(bookInstantly)

class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'request_date', 'requested_amount', 'paid_date', 'request_status')
    list_filter = ('request_date', 'paid_date', 'request_status')
    search_fields = ['id', 'request_date', 'request_status']  # Add more fields as needed

admin.site.register(PaymentRequest, PaymentRequestAdmin)
