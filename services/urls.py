from django.urls import path


from . import views

app_name = 'services'

urlpatterns = [
    path("", views.index, name="index"),
    path("vehicle_display", views.vehicleDisplay, name="vehicle_display"),
    path('detail/<int:car_id>', views.detail, name="detail"),
    path('booking', views.booking, name="booking"),
    path('submit-review/<int:vehicle_id>', views.submit_review, name="submitReview"),
    path('booking-request', views.booking_request, name="booking_request"), 
    path('request_payment/<int:booking_id>/', views.request_payment, name="request_payment"), 
    path('payment_failed', views.payment_failed, name="payment_failed"),
    path('payment_success/<int:booking_id>', views.payment_success, name="payment_success"),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('cancel_booking_by_vendor/<int:booking_id>/', views.cancel_booking_by_vendor, name='cancel_booking_by_vendor')
]
